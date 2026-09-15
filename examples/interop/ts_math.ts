// ts_math.ts — TypeScript 示例模块
// 用于演示 AuroraJS 对 TypeScript 的支持
// 编译: tsc ts_math.ts → ts_math.js
// 或直接: ts-node ts_math.ts

// 基本数学函数
export function add(a: number, b: number): number {
    return a + b;
}

export function subtract(a: number, b: number): number {
    return a - b;
}

export function multiply(a: number, b: number): number {
    return a * b;
}

export function divide(a: number, b: number): number {
    if (b === 0) throw new Error("Division by zero");
    return a / b;
}

// 数组操作
export function sum(numbers: number[]): number {
    return numbers.reduce((acc, n) => acc + n, 0);
}

export function average(numbers: number[]): number {
    if (numbers.length === 0) return 0;
    return sum(numbers) / numbers.length;
}

export function square(numbers: number[]): number[] {
    return numbers.map(n => n * n);
}

// 字符串操作
export function greet(name: string): string {
    return `Hello, ${name}!`;
}

export function toUpper(str: string): string {
    return str.toUpperCase();
}

// 对象操作
export interface Point {
    x: number;
    y: number;
}

export function distance(p1: Point, p2: Point): number {
    const dx = p2.x - p1.x;
    const dy = p2.y - p1.y;
    return Math.sqrt(dx * dx + dy * dy);
}

// 主入口(直接运行时执行)
if (require.main === module) {
    console.log("TypeScript Math Module");
    console.log("add(3, 4) =", add(3, 4));
    console.log("sum([1,2,3,4,5]) =", sum([1, 2, 3, 4, 5]));
    console.log("greet('Aurora') =", greet("Aurora"));
}
