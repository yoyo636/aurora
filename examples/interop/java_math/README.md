# Java 互操作示例

## 编译
```bash
cd examples/interop/java_math
javac MathUtils.java
```

## 直接运行
```bash
java MathUtils
```

## 在 Aurora 中调用

```aurora
import std.java

# 调用静态方法
std.java.call("MathUtils", "add", 3, 4)          # 7
std.java.call("MathUtils", "multiply", 5, 6)      # 30
std.java.call("MathUtils", "greet", "Aurora")     # "Hello, Aurora!"

# 运行主类
std.java.run("MathUtils", [], classpath=".")

# 编译源文件
std.java.compile("MathUtils.java")
```

## 类路径配置
如果类在其他目录或 jar 包中，通过 `classpath` 参数指定：

```aurora
std.java.call("com.example.MathUtils", "add", 3, 4, classpath="lib/mylib.jar:.")
```
