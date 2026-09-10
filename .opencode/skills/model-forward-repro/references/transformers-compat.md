# transformers 版本兼容排查手册

## 探测三板斧

```python
import transformers, inspect
print(transformers.__version__)
from transformers import XForConditionalGeneration
print(inspect.signature(XForConditionalGeneration.forward))
print(XForConditionalGeneration.__mro__)  # 确认基类链
```

## 已知断层（v4 → v5）

| 变化 | 症状 | build_model 桥接方式 |
|---|---|---|
| forward 移除 `output_attentions` / `output_hidden_states` 形参 | TypeError 或被 kwargs 吞掉后拿不到 hidden_states | 在桥接子类的 forward 中拦截这两个参数，显式传给基类或改为读取 `model_kwargs` 通道 |
| `past_key_values` 由 tuple-of-tuples 改为 Cache 对象 | 索引 `[layer][0]` 报错 | 用 `.layers[i].keys`；只读观察时可直接忽略 |
| `rope_deltas` 进入 CausalLMOutput dataclass（旧版没有） | 仓库代码手工构造输出对象时 TypeError | 传 `rope_deltas=outputs.rope_deltas`（v5 已有该字段） |
| 输出 dataclass 字段重排 | 位置索引 outputs[0]/[1] 含义漂移 | 一律改用属性访问 |
| 模型类移动模块路径（如 modeling_xxx 内部类改名） | ImportError | 在 build_model 中 try/except 双路径 import |

## ms-swift 版本不匹配（典型：仓库锁 3.x，本地 4.x）

**不要降级/升级 swift 迁就仓库。** swift 注册代码（register_model/template）只服务于训练循环；前向观察只需：
1. 从仓库拿 modeling_*.py 的纯模型类
2. 从 checkpoint 目录拿 config + processor/tokenizer
3. 在 `build_model.py` 中写桥接子类继承仓库类、重写 forward，绕开 swift 注册链路
4. 在 `build_input.py` 中手工构造 batch（参照 swift template 的 _encode 逻辑等价实现）

## 权重加载

- safetensors 分片缺 index.json → 手工从 config.json + 权重文件名推断
- bf16 在 CPU 上部分算子慢/不支持 → dtype 保持 bf16 只影响速度不影响 shape；若报错改 fp16，仍报错才 fp32（内存翻倍需评估）
- trust_remote_code：ModelScope 下载的 Qwen 官方权重不需要

## 采集侧通用坑

- forward hook 挂 `register_forward_hook(..., with_kwargs=True)` 才能看到传入子模块的 kwargs（如 position_ids）
- `torch.no_grad()` + `model.eval()`，否则 3B 模型梯度驻留内存爆炸
- hidden_states 有 37 层 × 序列长度，全量收集爆内存：hook 只记 shape 不保存张量引用
