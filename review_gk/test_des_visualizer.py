"""Đối chiếu HTML với des.py. Chạy: python review_gk/test_des_visualizer.py.

Chỉ dùng thư viện chuẩn Python và Node.js đã có trên máy; không cần npm install.
"""

import ast
import importlib.util
import json
from pathlib import Path
import random
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
PAGE = ROOT / "des_visualizer.html"
SOURCE = ROOT / "code" / "des.py"

NODE_CHECK = r"""
const fs = require('node:fs');
const vm = require('node:vm');
const {TextEncoder, TextDecoder} = require('node:util');
const html = fs.readFileSync(process.argv[1], 'utf8');
const data = JSON.parse(fs.readFileSync(0, 'utf8'));
const script = name => html.match(new RegExp('<script '+name+'>([\\s\\S]*?)</script>'))[1];
const tables = html.match(/<script id="des-tables" type="application\/json">([\s\S]*?)<\/script>/)[1];
const context = {document:{getElementById:()=>({textContent:tables})},TextEncoder,TextDecoder};
vm.createContext(context);
vm.runInContext(script('data-des-engine'),context);
new vm.Script(script('data-des-ui')); // Parse all UI JavaScript as well.
const d = context.DES;
const blocks = data.blocks.map(c=>{
 const keys=d.createKeys(c.key), t=d.transformBlock(c.block,keys,c.decrypt);
 return {output:t.output, ip:d.hex(t.ip,16), preoutput:d.hex(t.preoutput,16),
  keys:keys.rounds.map(r=>d.hex(r.key,12)),
  rounds:t.rounds.map(r=>({left:d.hex(r.left,8),right:d.hex(r.right,8),
   f:d.hex(r.f.result,8),nextLeft:d.hex(r.newLeft,8),nextRight:d.hex(r.newRight,8)}))};
});
const texts=data.texts.map(c=>{
 const result=d.encryptText(c.text,c.key), recovered=d.decryptText(result.cipher,c.key);
 return {cipher:result.cipher, pad:result.pad, byteLength:result.bytes.length, text:recovered.text};
});
let rejected=0;
for(const bad of data.bad){
 let threw=false;
 try {
  if(bad.type==='key')d.createKeys(bad.value);
  else if(bad.type==='block')d.transformBlock(bad.value,d.createKeys(data.blocks[0].key));
  else d.decryptText(bad.value,data.blocks[0].key);
 }catch{threw=true;}
 if(!threw)throw Error('Accepted invalid '+bad.type+': '+bad.value);
 rejected++;
}
// Exercise table mappings, including duplicate positions in E.
for(let value=0;value<256;value++){
 const bits=d.numberToBits(value,64), ip=d.permute(bits,d.TABLES.IP);
 if(JSON.stringify(d.permute(ip,d.TABLES.IP_INV))!==JSON.stringify(bits))throw Error('IP inverse mismatch');
}
process.stdout.write(JSON.stringify({blocks,texts,rejected}));
"""


def main() -> None:
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("reference_des", SOURCE)
    des = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(des)
    source_text = SOURCE.read_text(encoding="utf-8")
    html = PAGE.read_text(encoding="utf-8")
    assert "__DES_TABLES__" not in html and "__PYTHON_SOURCE__" not in html
    assert not re.search(r'<(?:script|link)[^>]+(?:src|href)="https?://', html)
    embedded = json.loads(re.search(
        r'<script id="python-source" type="application/json">(.*?)</script>', html, re.S
    ).group(1))
    expected_source = {
        node.name: ast.get_source_segment(source_text, node)
        for node in ast.parse(source_text).body if isinstance(node, ast.FunctionDef)
    }
    assert embedded == expected_source, "Mã Python nhúng phải khớp mã gốc."
    referenced_ids = set(re.findall(r"\$\('([^']+)'\)", html))
    declared_ids = re.findall(r'\bid="([^"]+)"', html)
    assert len(declared_ids) == len(set(declared_ids)), "ID HTML bị trùng."
    assert referenced_ids <= set(declared_ids), referenced_ids - set(declared_ids)
    rng = random.Random(20261015)
    key = "133457799BBCDFF1"
    blocks = [
        {"key": key, "block": "0123456789ABCDEF", "decrypt": False},
        {"key": key, "block": "85E813540F0AB405", "decrypt": True},
        {"key": "0000000000000000", "block": "0000000000000000", "decrypt": False},
        {"key": "FFFFFFFFFFFFFFFF", "block": "FFFFFFFFFFFFFFFF", "decrypt": False},
    ]
    for _ in range(32):
        blocks.append({
            "key": rng.randbytes(8).hex().upper(),
            "block": rng.randbytes(8).hex().upper(),
            "decrypt": bool(rng.getrandbits(1)),
        })
    samples = ["", "a", "1234567", "12345678", "123456789", "1234567812345678",
               "Xin chào DES!", "Tiếng Việt: ă â đ ê ô ơ ư", "\ufeffBOM ở đầu", "\0\0abc\0",
               "<script>alert('x')</script>", "🙂🚀", "A" * 512]
    texts = [{"text": value, "key": key} for value in samples]
    invalid_padding = des.ma_hoa_khoi(bytes(8), bytes.fromhex(key)).hex()
    invalid_utf8 = des.ma_hoa_khoi(b"\xff" + bytes([7]) * 7, bytes.fromhex(key)).hex()
    bad = [
        {"type": "key", "value": ""}, {"type": "key", "value": "1234"},
        {"type": "key", "value": "ZZ3457799BBCDFF1"},
        {"type": "block", "value": "0"}, {"type": "block", "value": "00" * 9},
        {"type": "cipher", "value": ""}, {"type": "cipher", "value": "AA"},
        {"type": "cipher", "value": "GG" * 8},
        {"type": "cipher", "value": invalid_padding},
        {"type": "cipher", "value": invalid_utf8},
    ]
    result = subprocess.run(
        ["node", "-e", NODE_CHECK, str(PAGE)],
        input=json.dumps({"blocks": blocks, "texts": texts, "bad": bad}),
        text=True, encoding="utf-8", capture_output=True, check=True,
    )
    actual = json.loads(result.stdout)
    for case, got in zip(blocks, actual["blocks"], strict=True):
        block, key_bytes = bytes.fromhex(case["block"]), bytes.fromhex(case["key"])
        keys = des._tao_khoa_con(key_bytes)
        assert got["keys"] == [f"{des._bit_thanh_so(k):012X}" for k in keys]
        expected = (des.giai_ma_khoi if case["decrypt"] else des.ma_hoa_khoi)(block, key_bytes)
        assert got["output"] == expected.hex().upper(), case
        ip = des._hoan_vi(des._byte_thanh_bit(block), des._DES_IP)
        assert got["ip"] == f"{des._bit_thanh_so(ip):016X}"
        left, right = ip[:32], ip[32:]
        ordered_keys = keys[::-1] if case["decrypt"] else keys
        for subkey, round_got in zip(ordered_keys, got["rounds"], strict=True):
            f_result = des._ham_f(right, subkey)
            next_right = des._xor(left, f_result)
            assert round_got == {
                "left": f"{des._bit_thanh_so(left):08X}",
                "right": f"{des._bit_thanh_so(right):08X}",
                "f": f"{des._bit_thanh_so(f_result):08X}",
                "nextLeft": f"{des._bit_thanh_so(right):08X}",
                "nextRight": f"{des._bit_thanh_so(next_right):08X}",
            }
            left, right = right, next_right
        assert got["preoutput"] == f"{des._bit_thanh_so(right + left):016X}"
    assert actual["blocks"][0]["output"] == "85E813540F0AB405"
    assert actual["blocks"][1]["output"] == "0123456789ABCDEF"
    for case, got in zip(texts, actual["texts"], strict=True):
        expected_cipher = des.ma_hoa(case["text"], bytes.fromhex(case["key"]))
        assert got["cipher"] == expected_cipher, case
        assert got["text"] == des.giai_ma(expected_cipher, bytes.fromhex(case["key"]))
        assert got["pad"] == 8 - len(case["text"].encode("utf-8")) % 8
        assert got["byteLength"] == len(case["text"].encode("utf-8"))
    assert actual["rejected"] == len(bad)
    print(f"PASS: {len(blocks)} blocks x 16 rounds match Python; {len(texts)} text cases; "
          f"{len(bad)} invalid cases; 256 IP/inverse cases; {len(expected_source)} source functions; JS syntax and HTML IDs.")


if __name__ == "__main__":
    main()
