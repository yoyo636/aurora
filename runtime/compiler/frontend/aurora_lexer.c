/*
 * Aurora 编译器前端 - 词法分析器实现
 */

#include "aurora_lexer.h"

/* Token 类型名称表 */
static const char* token_names[] = {
    "TOKEN_EOF",
    "TOKEN_IDENT",
    "TOKEN_INT",
    "TOKEN_FLOAT",
    "TOKEN_STRING",
    "TOKEN_CHAR",
    "TOKEN_BOOL",
    "TOKEN_NULL",
    "TOKEN_PLUS",
    "TOKEN_MINUS",
    "TOKEN_STAR",
    "TOKEN_SLASH",
    "TOKEN_PERCENT",
    "TOKEN_AMP",
    "TOKEN_PIPE",
    "TOKEN_CARET",
    "TOKEN_TILDE",
    "TOKEN_BANG",
    "TOKEN_EQ",
    "TOKEN_LT",
    "TOKEN_GT",
    "TOKEN_PLUS_EQ",
    "TOKEN_MINUS_EQ",
    "TOKEN_STAR_EQ",
    "TOKEN_SLASH_EQ",
    "TOKEN_PERCENT_EQ",
    "TOKEN_AMP_EQ",
    "TOKEN_PIPE_EQ",
    "TOKEN_CARET_EQ",
    "TOKEN_EQ_EQ",
    "TOKEN_BANG_EQ",
    "TOKEN_LT_EQ",
    "TOKEN_GT_EQ",
    "TOKEN_AMP_AMP",
    "TOKEN_PIPE_PIPE",
    "TOKEN_LT_LT",
    "TOKEN_GT_GT",
    "TOKEN_LPAREN",
    "TOKEN_RPAREN",
    "TOKEN_LBRACE",
    "TOKEN_RBRACE",
    "TOKEN_LBRACKET",
    "TOKEN_RBRACKET",
    "TOKEN_COMMA",
    "TOKEN_SEMICOLON",
    "TOKEN_COLON",
    "TOKEN_DOT",
    "TOKEN_DOT_DOT",
    "TOKEN_ARROW",
    "TOKEN_FAT_ARROW",
    "TOKEN_QUESTION",
    "TOKEN_HASH",
    "TOKEN_AT",
    "TOKEN_DOLLAR",
    "TOKEN_BACKTICK",
    "TOKEN_BACKSLASH",
    "TOKEN_KW_LET",
    "TOKEN_KW_MUT",
    "TOKEN_KW_CONST",
    "TOKEN_KW_FN",
    "TOKEN_KW_RETURN",
    "TOKEN_KW_IF",
    "TOKEN_KW_ELSE",
    "TOKEN_KW_WHILE",
    "TOKEN_KW_FOR",
    "TOKEN_KW_LOOP",
    "TOKEN_KW_BREAK",
    "TOKEN_KW_CONTINUE",
    "TOKEN_KW_STRUCT",
    "TOKEN_KW_ENUM",
    "TOKEN_KW_TRAIT",
    "TOKEN_KW_IMPL",
    "TOKEN_KW_USE",
    "TOKEN_KW_MOD",
    "TOKEN_KW_PUB",
    "TOKEN_KW_PRIV",
    "TOKEN_KW_SELF",
    "TOKEN_KW_SUPER",
    "TOKEN_KW_CRATE",
    "TOKEN_KW_IN",
    "TOKEN_KW_AS",
    "TOKEN_KW_MATCH",
    "TOKEN_KW_WHERE",
    "TOKEN_KW_TYPE",
    "TOKEN_KW_TYPEOF",
    "TOKEN_KW_SIZEOF",
    "TOKEN_KW_ALIGNOF",
    "TOKEN_KW_UNSAFE",
    "TOKEN_KW_EXTERN",
    "TOKEN_KW_NATIVE",
    "TOKEN_KW_IMPORT",
    "TOKEN_KW_EXPORT",
    "TOKEN_KW_FROM",
    "TOKEN_KW_DEFAULT",
    "TOKEN_KW_STATIC",
    "TOKEN_KW_VOLATILE",
    "TOKEN_KW_INLINE",
    "TOKEN_KW_NOINLINE",
    "TOKEN_KW_COLD",
    "TOKEN_KW_HOT",
    "TOKEN_KW_PURE",
    "TOKEN_KW_IMPURE",
    "TOKEN_KW_NONNULL",
    "TOKEN_KW_NULLABLE",
    "TOKEN_KW_MOVE",
    "TOKEN_KW_COPY",
    "TOKEN_KW_CLONE",
    "TOKEN_KW_DROP",
    "TOKEN_KW_NEW",
    "TOKEN_KW_DELETE",
    "TOKEN_KW_MALLOC",
    "TOKEN_KW_FREE",
    "TOKEN_KW_ALLOC",
    "TOKEN_KW_DEALLOC",
    "TOKEN_KW_REALLOC",
    "TOKEN_KW_ZERO",
    "TOKEN_KW_UNINIT",
    "TOKEN_KW_ASSUME",
    "TOKEN_KW_UNREACHABLE",
    "TOKEN_KW_ABORT",
    "TOKEN_KW_PANIC",
    "TOKEN_KW_UNWRAP",
    "TOKEN_KW_EXPECT",
    "TOKEN_KW_TRY",
    "TOKEN_KW_CATCH",
    "TOKEN_KW_THROW",
    "TOKEN_KW_RAISE",
    "TOKEN_KW_RESCUE",
    "TOKEN_KW_ENSURE",
    "TOKEN_KW_FINALLY",
    "TOKEN_KW_DEFER",
    "TOKEN_KW_YIELD",
    "TOKEN_KW_AWAIT",
    "TOKEN_KW_ASYNC",
    "TOKEN_KW_SYNC",
    "TOKEN_KW_GO",
    "TOKEN_KW_SPAWN",
    "TOKEN_KW_JOIN",
    "TOKEN_KW_SELECT",
    "TOKEN_KW_CASE",
    "TOKEN_KW_SWITCH",
    "TOKEN_KW_GOTO",
    "TOKEN_KW_LABEL",
    "TOKEN_KW_MACRO",
    "TOKEN_KW_QUOTE",
    "TOKEN_KW_UNQUOTE",
    "TOKEN_KW_SPLICE",
    "TOKEN_KW_EVAL",
    "TOKEN_KW_EXEC",
    "TOKEN_KW_SHELL",
    "TOKEN_KW_CMD",
    "TOKEN_KW_PRINT",
    "TOKEN_KW_PRINTLN",
    "TOKEN_KW_EPRINT",
    "TOKEN_KW_EPRINTLN",
    "TOKEN_KW_ASSERT",
    "TOKEN_KW_DEBUG",
    "TOKEN_KW_TRACE",
    "TOKEN_KW_INFO",
    "TOKEN_KW_WARN",
    "TOKEN_KW_ERROR",
    "TOKEN_KW_FATAL",
    "TOKEN_KW_LOG",
    "TOKEN_KW_TRUE",
    "TOKEN_KW_FALSE",
    "TOKEN_KW_NONE",
    "TOKEN_KW_NIL",
    "TOKEN_KW_UNDEFINED",
    "TOKEN_KW_VOID",
    "TOKEN_KW_UNIT",
    "TOKEN_KW_NEVER",
    "TOKEN_KW_ANY",
    "TOKEN_KW_UNKNOWN",
    "TOKEN_KW_INFER",
    "TOKEN_KW_AUTO",
    "TOKEN_KW_DYN",
    "TOKEN_KW_IMPL_TRAIT",
    "TOKEN_KW_DYN_TRAIT",
    "TOKEN_KW_GENERIC",
    "TOKEN_KW_TEMPLATE",
    "TOKEN_KW_TYPENAME",
    "TOKEN_KW_CLASS",
    "TOKEN_KW_OBJECT",
    "TOKEN_KW_INTERFACE",
    "TOKEN_KW_PROTOCOL",
    "TOKEN_KW_EXTENSION",
    "TOKEN_KW_CATEGORY",
    "TOKEN_KW_SUBCLASS",
    "TOKEN_KW_SUPERCLASS",
    "TOKEN_KW_INHERIT",
    "TOKEN_KW_EXTENDS",
    "TOKEN_KW_IMPLEMENTS",
    "TOKEN_KW_CONFORMS",
    "TOKEN_KW_ADOPTS",
    "TOKEN_KW_SATISFIES",
    "TOKEN_KW_DERIVES",
    "TOKEN_KW_INHERITS",
    "TOKEN_KW_OVERRIDE",
    "TOKEN_KW_VIRTUAL",
    "TOKEN_KW_ABSTRACT",
    "TOKEN_KW_FINAL",
    "TOKEN_KW_SEALED",
    "TOKEN_KW_OPEN",
    "TOKEN_KW_CLOSED",
    "TOKEN_KW_INTERNAL",
    "TOKEN_KW_PROTECTED",
    "TOKEN_KW_PACKAGE",
    "TOKEN_KW_FILEPRIVATE",
    "TOKEN_KW_PRIVATE_SET",
    "TOKEN_KW_GET",
    "TOKEN_KW_SET",
    "TOKEN_KW_WILL_SET",
    "TOKEN_KW_DID_SET",
    "TOKEN_KW_LAZY",
    "TOKEN_KW_WEAK",
    "TOKEN_KW_UNOWNED",
    "TOKEN_KW_STRONG",
    "TOKEN_KW_RETAIN",
    "TOKEN_KW_RELEASE",
    "TOKEN_KW_AUTORELEASE",
    "TOKEN_KW_DEALLOC",
    "TOKEN_KW_DEINIT",
    "TOKEN_KW_FINALIZE",
    "TOKEN_KW_DISPOSE",
    "TOKEN_KW_CLOSE",
    "TOKEN_KW_OPEN_KW",
    "TOKEN_KW_READ",
    "TOKEN_KW_WRITE",
    "TOKEN_KW_APPEND",
    "TOKEN_KW_FLUSH",
    "TOKEN_KW_SEEK",
    "TOKEN_KW_TELL",
    "TOKEN_KW_EOF",
    "TOKEN_KW_REWIND",
    "TOKEN_KW_TRUNCATE",
    "TOKEN_KW_SYNC",
    "TOKEN_KW_DATASYNC",
    "TOKEN_KW_FSYNC",
    "TOKEN_KW_FDATASYNC",
    "TOKEN_KW_MSYNC",
    "TOKEN_KW_MMAP",
    "TOKEN_KW_MUNMAP",
    "TOKEN_KW_MPROTECT",
    "TOKEN_KW_MLOCK",
    "TOKEN_KW_MUNLOCK",
    "TOKEN_KW_MADVISE",
    "TOKEN_KW_MINCORE",
    "TOKEN_KW_MREMAP",
    "TOKEN_KW_MREMAP_FIXED",
    "TOKEN_KW_MREMAP_MAYMOVE",
    "TOKEN_KW_MREMAP_DONTUNMAP",
    "TOKEN_KW_SHM_OPEN",
    "TOKEN_KW_SHM_UNLINK",
    "TOKEN_KW_SEM_OPEN",
    "TOKEN_KW_SEM_CLOSE",
    "TOKEN_KW_SEM_UNLINK",
    "TOKEN_KW_SEM_WAIT",
    "TOKEN_KW_SEM_TRYWAIT",
    "TOKEN_KW_SEM_POST",
    "TOKEN_KW_SEM_GETVALUE",
    "TOKEN_KW_SEM_INIT",
    "TOKEN_KW_SEM_DESTROY",
    "TOKEN_KW_MUTEX_INIT",
    "TOKEN_KW_MUTEX_DESTROY",
    "TOKEN_KW_MUTEX_LOCK",
    "TOKEN_KW_MUTEX_TRYLOCK",
    "TOKEN_KW_MUTEX_UNLOCK",
    "TOKEN_KW_MUTEX_TIMEDLOCK",
    "TOKEN_KW_COND_INIT",
    "TOKEN_KW_COND_DESTROY",
    "TOKEN_KW_COND_WAIT",
    "TOKEN_KW_COND_TIMEDWAIT",
    "TOKEN_KW_COND_SIGNAL",
    "TOKEN_KW_COND_BROADCAST",
    "TOKEN_KW_RWLOCK_INIT",
    "TOKEN_KW_RWLOCK_DESTROY",
    "TOKEN_KW_RWLOCK_RDLOCK",
    "TOKEN_KW_RWLOCK_WRLOCK",
    "TOKEN_KW_RWLOCK_UNLOCK",
    "TOKEN_KW_RWLOCK_TRYRDLOCK",
    "TOKEN_KW_RWLOCK_TRYWRLOCK",
    "TOKEN_KW_SPIN_INIT",
    "TOKEN_KW_SPIN_DESTROY",
    "TOKEN_KW_SPIN_LOCK",
    "TOKEN_KW_SPIN_TRYLOCK",
    "TOKEN_KW_SPIN_UNLOCK",
    "TOKEN_KW_BARRIER_INIT",
    "TOKEN_KW_BARRIER_DESTROY",
    "TOKEN_KW_BARRIER_WAIT",
    "TOKEN_KW_ONCE_INIT",
    "TOKEN_KW_ONCE",
    "TOKEN_KW_CLEANUP_PUSH",
    "TOKEN_KW_CLEANUP_POP",
    "TOKEN_KW_KEY_CREATE",
    "TOKEN_KW_KEY_DELETE",
    "TOKEN_KW_KEY_SETSPECIFIC",
    "TOKEN_KW_KEY_GETSPECIFIC",
    "TOKEN_KW_THREAD_CREATE",
    "TOKEN_KW_THREAD_JOIN",
    "TOKEN_KW_THREAD_DETACH",
    "TOKEN_KW_THREAD_EXIT",
    "TOKEN_KW_THREAD_SELF",
    "TOKEN_KW_THREAD_EQUAL",
    "TOKEN_KW_THREAD_YIELD",
    "TOKEN_KW_THREAD_SETCONCURRENCY",
    "TOKEN_KW_THREAD_GETCONCURRENCY",
    "TOKEN_KW_THREAD_SETSCHEDPARAM",
    "TOKEN_KW_THREAD_GETSCHEDPARAM",
    "TOKEN_KW_THREAD_SETSCHEDPRIO",
    "TOKEN_KW_THREAD_GETCPUCLOCKID",
    "TOKEN_KW_THREAD_ATTR_INIT",
    "TOKEN_KW_THREAD_ATTR_DESTROY",
    "TOKEN_KW_THREAD_ATTR_SETDETACHSTATE",
    "TOKEN_KW_THREAD_ATTR_GETDETACHSTATE",
    "TOKEN_KW_THREAD_ATTR_SETSTACKSIZE",
    "TOKEN_KW_THREAD_ATTR_GETSTACKSIZE",
    "TOKEN_KW_THREAD_ATTR_SETSTACK",
    "TOKEN_KW_THREAD_ATTR_GETSTACK",
    "TOKEN_KW_THREAD_ATTR_SETGUARDSIZE",
    "TOKEN_KW_THREAD_ATTR_GETGUARDSIZE",
    "TOKEN_KW_THREAD_ATTR_SETSCOPE",
    "TOKEN_KW_THREAD_ATTR_GETSCOPE",
    "TOKEN_KW_THREAD_ATTR_SETINHERITSCHED",
    "TOKEN_KW_THREAD_ATTR_GETINHERITSCHED",
    "TOKEN_KW_THREAD_ATTR_SETSCHEDPOLICY",
    "TOKEN_KW_THREAD_ATTR_GETSCHEDPOLICY",
    "TOKEN_KW_THREAD_ATTR_SETSCHEDPARAM",
    "TOKEN_KW_THREAD_ATTR_GETSCHEDPARAM",
    "TOKEN_KW_THREAD_ATTR_SETAFFINITY_NP",
    "TOKEN_KW_THREAD_ATTR_GETAFFINITY_NP",
    "TOKEN_KW_THREAD_SETAFFINITY_NP",
    "TOKEN_KW_THREAD_GETAFFINITY_NP",
    "TOKEN_KW_THREAD_ATTR_SETNAME_NP",
    "TOKEN_KW_THREAD_ATTR_GETNAME_NP",
    "TOKEN_KW_THREAD_SETNAME_NP",
    "TOKEN_KW_THREAD_GETNAME_NP",
    "TOKEN_KW_THREAD_SETSTACKADDR_NP",
    "TOKEN_KW_THREAD_GETSTACKADDR_NP",
    "TOKEN_KW_THREAD_SETSTACKSIZE_NP",
    "TOKEN_KW_THREAD_GETSTACKSIZE_NP",
    "TOKEN_KW_THREAD_SETCANCELSTATE",
    "TOKEN_KW_THREAD_GETCANCELSTATE",
    "TOKEN_KW_THREAD_SETCANCELTYPE",
    "TOKEN_KW_THREAD_GETCANCELTYPE",
    "TOKEN_KW_THREAD_CANCEL",
    "TOKEN_KW_THREAD_TESTCANCEL",
    "TOKEN_KW_THREAD_CLEANUP_PUSH",
    "TOKEN_KW_THREAD_CLEANUP_POP",
    "TOKEN_KW_THREAD_SIGMASK",
    "TOKEN_KW_THREAD_KILL",
    "TOKEN_KW_THREAD_SIGQUEUE",
    "TOKEN_KW_PTHREAD_ATFORK",
    "TOKEN_KW_FORK",
    "TOKEN_KW_EXEC",
    "TOKEN_KW_EXECL",
    "TOKEN_KW_EXECV",
    "TOKEN_KW_EXECLE",
    "TOKEN_KW_EXECVE",
    "TOKEN_KW_EXECLP",
    "TOKEN_KW_EXECVP",
    "TOKEN_KW_EXECVPE",
    "TOKEN_KW_FEXECVE",
    "TOKEN_KW_WAIT",
    "TOKEN_KW_WAITPID",
    "TOKEN_KW_WAITID",
    "TOKEN_KW_WAIT3",
    "TOKEN_KW_WAIT4",
    "TOKEN_KW_EXIT",
    "TOKEN_KW__EXIT",
    "TOKEN_KW__EXITGROUP",
    "TOKEN_KW_ATEXIT",
    "TOKEN_KW_ON_EXIT",
    "TOKEN_KW_GETPID",
    "TOKEN_KW_GETPPID",
    "TOKEN_KW_GETPGID",
    "TOKEN_KW_SETPGID",
    "TOKEN_KW_GETPGRP",
    "TOKEN_KW_SETPGRP",
    "TOKEN_KW_GETSID",
    "TOKEN_KW_SETSID",
    "TOKEN_KW_GETUID",
    "TOKEN_KW_SETEUID",
    "TOKEN_KW_GETEUID",
    "TOKEN_KW_SETUID",
    "TOKEN_KW_GETGID",
    "TOKEN_KW_SETEGID",
    "TOKEN_KW_GETEGID",
    "TOKEN_KW_SETGID",
    "TOKEN_KW_GETGROUPS",
    "TOKEN_KW_SETGROUPS",
    "TOKEN_KW_GETLOGIN",
    "TOKEN_KW_SETLOGIN",
    "TOKEN_KW_GETPWNAM",
    "TOKEN_KW_GETPWUID",
    "TOKEN_KW_GETGRNAM",
    "TOKEN_KW_GETGRGID",
    "TOKEN_KW_GETHOSTNAME",
    "TOKEN_KW_SETHOSTNAME",
    "TOKEN_KW_GETDOMAINNAME",
    "TOKEN_KW_SETDOMAINNAME",
    "TOKEN_KW_UNAME",
    "TOKEN_KW_SYSINFO",
    "TOKEN_KW_GETRUSAGE",
    "TOKEN_KW_GETRUSAGE_CHILDREN",
    "TOKEN_KW_GETRUSAGE_THREAD",
    "TOKEN_KW_TIMES",
    "TOKEN_KW_CLOCK",
    "TOKEN_KW_CLOCK_GETTIME",
    "TOKEN_KW_CLOCK_SETTIME",
    "TOKEN_KW_CLOCK_GETRES",
    "TOKEN_KW_CLOCK_ADJTIME",
    "TOKEN_KW_NANOSLEEP",
    "TOKEN_KW_USLEEP",
    "TOKEN_KW_SLEEP",
    "TOKEN_KW_ALARM",
    "TOKEN_KW_SETITIMER",
    "TOKEN_KW_GETITIMER",
    "TOKEN_KW_TIMER_CREATE",
    "TOKEN_KW_TIMER_DELETE",
    "TOKEN_KW_TIMER_SETTIME",
    "TOKEN_KW_TIMER_GETTIME",
    "TOKEN_KW_TIMER_GETOVERRUN",
    "TOKEN_KW_SIGNAL",
    "TOKEN_KW_SIGACTION",
    "TOKEN_KW_SIGPROCMASK",
    "TOKEN_KW_SIGPENDING",
    "TOKEN_KW_SIGSUSPEND",
    "TOKEN_KW_SIGWAIT",
    "TOKEN_KW_SIGWAITINFO",
    "TOKEN_KW_SIGTIMEDWAIT",
    "TOKEN_KW_SIGQUEUE",
    "TOKEN_KW_SIGKILL",
    "TOKEN_KW_SIGSTOP",
    "TOKEN_KW_SIGCONT",
    "TOKEN_KW_SIGINT",
    "TOKEN_KW_SIGTERM",
    "TOKEN_KW_SIGABRT",
    "TOKEN_KW_SIGSEGV",
    "TOKEN_KW_SIGFPE",
    "TOKEN_KW_SIGILL",
    "TOKEN_KW_SIGBUS",
    "TOKEN_KW_SIGPIPE",
    "TOKEN_KW_SIGALRM",
    "TOKEN_KW_SIGCHLD",
    "TOKEN_KW_SIGHUP",
    "TOKEN_KW_SIGQUIT",
    "TOKEN_KW_SIGTRAP",
    "TOKEN_KW_SIGSYS",
    "TOKEN_KW_SIGURG",
    "TOKEN_KW_SIGXCPU",
    "TOKEN_KW_SIGXFSZ",
    "TOKEN_KW_SIGVTALRM",
    "TOKEN_KW_SIGPROF",
    "TOKEN_KW_SIGWINCH",
    "TOKEN_KW_SIGIO",
    "TOKEN_KW_SIGPOLL",
    "TOKEN_KW_SIGPWR",
    "TOKEN_KW_SIGUNUSED",
    "TOKEN_KW_SIGRTMIN",
    "TOKEN_KW_SIGRTMAX",
    "TOKEN_KW_SIGEMPTYSET",
    "TOKEN_KW_SIGFILLSET",
    "TOKEN_KW_SIGADDSET",
    "TOKEN_KW_SIGDELSET",
    "TOKEN_KW_SIGISMEMBER",
    "TOKEN_KW_SIGSETOPS",
    "TOKEN_KW_PAUSE",
    "TOKEN_KW_KILL",
    "TOKEN_KW_KILLPG",
    "TOKEN_KW_RAISE",
    "TOKEN_KW_SIGSETJMP",
    "TOKEN_KW_SIGLONGJMP",
    "TOKEN_KW_SETJMP",
    "TOKEN_KW_LONGJMP",
    "TOKEN_KW___BUILTIN_SETJMP",
    "TOKEN_KW___BUILTIN_LONGJMP",
    "TOKEN_KW___BUILTIN_RETURN_ADDRESS",
    "TOKEN_KW___BUILTIN_FRAME_ADDRESS",
    "TOKEN_KW___BUILTIN_EXPECT",
    "TOKEN_KW___BUILTIN_EXPECT_WITH_PROBABILITY",
    "TOKEN_KW___BUILTIN_UNREACHABLE",
    "TOKEN_KW___BUILTIN_TRAP",
    "TOKEN_KW___BUILTIN_ABORT",
    "TOKEN_KW___BUILTIN_ASSUME",
    "TOKEN_KW___BUILTIN_ASSUME_ALIGNED",
    "TOKEN_KW___BUILTIN_PREFETCH",
    "TOKEN_KW___BUILTIN_CLZ",
    "TOKEN_KW___BUILTIN_CTZ",
    "TOKEN_KW___BUILTIN_POPCOUNT",
    "TOKEN_KW___BUILTIN_PARITY",
    "TOKEN_KW___BUILTIN_FFS",
    "TOKEN_KW___BUILTIN_BSWAP",
    "TOKEN_KW___BUILTIN_BSWAP16",
    "TOKEN_KW___BUILTIN_BSWAP32",
    "TOKEN_KW___BUILTIN_BSWAP64",
    "TOKEN_KW___BUILTIN_BYTEORDER",
    "TOKEN_KW___BUILTIN_ENDIAN",
    "TOKEN_KW___BUILTIN_NTOHS",
    "TOKEN_KW___BUILTIN_HTONS",
    "TOKEN_KW___BUILTIN_NTOHL",
    "TOKEN_KW___BUILTIN_HTONL",
    "TOKEN_KW___BUILTIN_CONSTANT_P",
    "TOKEN_KW___BUILTIN_CHOOSE_EXPR",
    "TOKEN_KW___BUILTIN_TYPES_COMPATIBLE_P",
    "TOKEN_KW___BUILTIN_IS_CONSTANT",
    "TOKEN_KW___BUILTIN_HAS_ATTRIBUTE",
    "TOKEN_KW___BUILTIN_HAS_FEATURE",
    "TOKEN_KW___BUILTIN_HAS_INCLUDE",
    "TOKEN_KW___BUILTIN_HAS_EXTENSION",
    "TOKEN_KW___BUILTIN_HAS_WARNING",
    "TOKEN_KW___BUILTIN_HAS_DECLSPEC",
    "TOKEN_KW___BUILTIN_HAS_CPP_ATTRIBUTE",
    "TOKEN_KW___BUILTIN_LINE",
    "TOKEN_KW___BUILTIN_FILE",
    "TOKEN_KW___BUILTIN_FUNCTION",
    "TOKEN_KW___BUILTIN_FUNC",
    "TOKEN_KW___BUILTIN_PRETTY_FUNCTION",
    "TOKEN_KW___BUILTIN_COLUMN",
    "TOKEN_KW___BUILTIN_COMPILER",
    "TOKEN_KW___BUILTIN_VERSION",
    "TOKEN_KW___BUILTIN_TIMESTAMP",
    "TOKEN_KW___BUILTIN_DATE",
    "TOKEN_KW___BUILTIN_TIME",
    "TOKEN_KW___BUILTIN_STDC_HOSTED",
    "TOKEN_KW___BUILTIN_STDC_VERSION",
    "TOKEN_KW___BUILTIN_STDC_UTF_16",
    "TOKEN_KW___BUILTIN_STDC_UTF_32",
    "TOKEN_KW___BUILTIN_STDC_NO_ATOMICS",
    "TOKEN_KW___BUILTIN_STDC_NO_COMPLEX",
    "TOKEN_KW___BUILTIN_STDC_NO_THREADS",
    "TOKEN_KW___BUILTIN_STDC_NO_VLA",
    "TOKEN_KW___BUILTIN_STDC_IEC_559",
    "TOKEN_KW___BUILTIN_STDC_IEC_559_COMPLEX",
    "TOKEN_KW___BUILTIN_STDC_ISO_10646",
    "TOKEN_KW___BUILTIN_STDC_LIB_EXT1",
    "TOKEN_KW___BUILTIN_STDC_ANALYZABLE",
    "TOKEN_KW___BUILTIN_STDC_WANT_LIB_EXT1",
    "TOKEN_KW___BUILTIN_STDC_MATH_H",
    "TOKEN_KW___BUILTIN_STDC_MATH_ERRNO",
    "TOKEN_KW___BUILTIN_STDC_MATH_ERREXCEPT",
    "TOKEN_KW___BUILTIN_STDC_MATH_FENV_ACCESS",
    "TOKEN_KW___BUILTIN_STDC_MATH_FAST_MATH",
    "TOKEN_KW___BUILTIN_STDC_MATH_FINITE_MATH_ONLY",
    "TOKEN_KW___BUILTIN_STDC_MATH_CONTRACT",
    "TOKEN_KW___BUILTIN_STDC_MATH_EVAL_METHOD",
    "TOKEN_KW___BUILTIN_STDC_MATH_FENV_ROUND",
    "TOKEN_KW___BUILTIN_STDC_MATH_FENV_TRAPS",
    "TOKEN_KW___BUILTIN_STDC_MATH_FENV_DETERM",
    "TOKEN_KW___BUILTIN_STDC_MATH_FENV_CX_LIMITED_RANGE",
    "TOKEN_KW___BUILTIN_STDC_MATH_FENV_CX_FINITE_MATH_ONLY",
    "TOKEN_KW___BUILTIN_STDC_MATH_FENV_CX_CONTRACT",
    "TOKEN_KW___BUILTIN_STDC_MATH_FENV_CX_EVAL_METHOD",
    "TOKEN_KW___BUILTIN_STDC_MATH_FENV_CX_FENV_ROUND",
    "TOKEN_KW___BUILTIN_STDC_MATH_FENV_CX_FENV_TRAPS",
    "TOKEN_KW___BUILTIN_STDC_MATH_FENV_CX_FENV_DETERM",
    "TOKEN_KW___BUILTIN_STDC_MATH_FENV_CX_CX_LIMITED_RANGE",
    "TOKEN_KW___BUILTIN_STDC_MATH_FENV_CX_CX_FINITE_MATH_ONLY",
};

/* Token 类型描述表 */
static const char* token_descriptions[] = {
    "文件结束",
    "标识符",
    "整数",
    "浮点数",
    "字符串",
    "字符",
    "布尔",
    "空值",
    "+",
    "-",
    "*",
    "/",
    "%",
    "&",
    "|",
    "^",
    "~",
    "!",
    "=",
    "<",
    ">",
    "+=",
    "-=",
    "*=",
    "/=",
    "%=",
    "&=",
    "|=",
    "^=",
    "==",
    "!=",
    "<=",
    ">=",
    "&&",
    "||",
    "<<",
    ">>",
    "(",
    ")",
    "{",
    "}",
    "[",
    "]",
    ",",
    ";",
    ":",
    ".",
    "..",
    "->",
    "=>",
    "?",
    "#",
    "@",
    "$",
    "`",
    "\",
    "let",
    "mut",
    "const",
    "fn",
    "return",
    "if",
    "else",
    "while",
    "for",
    "loop",
    "break",
    "continue",
    "struct",
    "enum",
    "trait",
    "impl",
    "use",
    "mod",
    "pub",
    "priv",
    "self",
    "super",
    "crate",
    "in",
    "as",
    "match",
    "where",
    "type",
    "typeof",
    "sizeof",
    "alignof",
    "unsafe",
    "extern",
    "native",
    "import",
    "export",
    "from",
    "default",
    "static",
    "volatile",
    "inline",
    "noinline",
    "cold",
    "hot",
    "pure",
    "impure",
    "nonnull",
    "nullable",
    "move",
    "copy",
    "clone",
    "drop",
    "new",
    "delete",
    "malloc",
    "free",
    "alloc",
    "dealloc",
    "realloc",
    "zero",
    "uninit",
    "assume",
    "unreachable",
    "abort",
    "panic",
    "unwrap",
    "expect",
    "try",
    "catch",
    "throw",
    "raise",
    "rescue",
    "ensure",
    "finally",
    "defer",
    "yield",
    "await",
    "async",
    "sync",
    "go",
    "spawn",
    "join",
    "select",
    "case",
    "switch",
    "goto",
    "label",
    "macro",
    "quote",
    "unquote",
    "splice",
    "eval",
    "exec",
    "shell",
    "cmd",
    "print",
    "println",
    "eprint",
    "eprintln",
    "assert",
    "debug",
    "trace",
    "info",
    "warn",
    "error",
    "fatal",
    "log",
    "true",
    "false",
    "none",
    "nil",
    "undefined",
    "void",
    "unit",
    "never",
    "any",
    "unknown",
    "infer",
    "auto",
    "dyn",
    "impl trait",
    "dyn trait",
    "generic",
    "template",
    "typename",
    "class",
    "object",
    "interface",
    "protocol",
    "extension",
    "category",
    "subclass",
    "superclass",
    "inherit",
    "extends",
    "implements",
    "conforms",
    "adopts",
    "satisfies",
    "derives",
    "inherits",
    "override",
    "virtual",
    "abstract",
    "final",
    "sealed",
    "open",
    "closed",
    "internal",
    "protected",
    "package",
    "fileprivate",
    "private(set)",
    "get",
    "set",
    "willSet",
    "didSet",
    "lazy",
    "weak",
    "unowned",
    "strong",
    "retain",
    "release",
    "autorelease",
    "dealloc",
    "deinit",
    "finalize",
    "dispose",
    "close",
    "open (keyword)",
    "read",
    "write",
    "append",
    "flush",
    "seek",
    "tell",
    "eof",
    "rewind",
    "truncate",
    "sync (keyword)",
    "datasync",
    "fsync",
    "fdatasync",
    "msync",
    "mmap",
    "munmap",
    "mprotect",
    "mlock",
    "munlock",
    "madvise",
    "mincore",
    "mremap",
    "mremap_fixed",
    "mremap_maymove",
    "mremap_dontunmap",
    "shm_open",
    "shm_unlink",
    "sem_open",
    "sem_close",
    "sem_unlink",
    "sem_wait",
    "sem_trywait",
    "sem_post",
    "sem_getvalue",
    "sem_init",
    "sem_destroy",
    "mutex_init",
    "mutex_destroy",
    "mutex_lock",
    "mutex_trylock",
    "mutex_unlock",
    "mutex_timedlock",
    "cond_init",
    "cond_destroy",
    "cond_wait",
    "cond_timedwait",
    "cond_signal",
    "cond_broadcast",
    "rwlock_init",
    "rwlock_destroy",
    "rwlock_rdlock",
    "rwlock_wrlock",
    "rwlock_unlock",
    "rwlock_tryrdlock",
    "rwlock_trywrlock",
    "spin_init",
    "spin_destroy",
    "spin_lock",
    "spin_trylock",
    "spin_unlock",
    "barrier_init",
    "barrier_destroy",
    "barrier_wait",
    "once_init",
    "once",
    "cleanup_push",
    "cleanup_pop",
    "key_create",
    "key_delete",
    "key_setspecific",
    "key_getspecific",
    "thread_create",
    "thread_join",
    "thread_detach",
    "thread_exit",
    "thread_self",
    "thread_equal",
    "thread_yield",
    "thread_setconcurrency",
    "thread_getconcurrency",
    "thread_setschedparam",
    "thread_getschedparam",
    "thread_setschedprio",
    "thread_getcpuclockid",
    "thread_attr_init",
    "thread_attr_destroy",
    "thread_attr_setdetachstate",
    "thread_attr_getdetachstate",
    "thread_attr_setstacksize",
    "thread_attr_getstacksize",
    "thread_attr_setstack",
    "thread_attr_getstack",
    "thread_attr_setguardsize",
    "thread_attr_getguardsize",
    "thread_attr_setscope",
    "thread_attr_getscope",
    "thread_attr_setinheritsched",
    "thread_attr_getinheritsched",
    "thread_attr_setschedpolicy",
    "thread_attr_getschedpolicy",
    "thread_attr_setschedparam",
    "thread_attr_getschedparam",
    "thread_attr_setaffinity_np",
    "thread_attr_getaffinity_np",
    "thread_setaffinity_np",
    "thread_getaffinity_np",
    "thread_attr_setname_np",
    "thread_attr_getname_np",
    "thread_setname_np",
    "thread_getname_np",
    "thread_setstackaddr_np",
    "thread_getstackaddr_np",
    "thread_setstacksize_np",
    "thread_getstacksize_np",
    "thread_setcancelstate",
    "thread_getcancelstate",
    "thread_setcanceltype",
    "thread_getcanceltype",
    "thread_cancel",
    "thread_testcancel",
    "thread_cleanup_push",
    "thread_cleanup_pop",
    "thread_sigmask",
    "thread_kill",
    "thread_sigqueue",
    "pthread_atfork",
    "fork",
    "exec",
    "execl",
    "execv",
    "execle",
    "execve",
    "execlp",
    "execvp",
    "execvpe",
    "fexecve",
    "wait",
    "waitpid",
    "waitid",
    "wait3",
    "wait4",
    "exit",
    "_exit",
    "_exit_group",
    "atexit",
    "on_exit",
    "getpid",
    "getppid",
    "getpgid",
    "setpgid",
    "getpgrp",
    "setpgrp",
    "getsid",
    "setsid",
    "getuid",
    "seteuid",
    "geteuid",
    "setuid",
    "getgid",
    "setegid",
    "getegid",
    "setgid",
    "getgroups",
    "setgroups",
    "getlogin",
    "setlogin",
    "getpwnam",
    "getpwuid",
    "getgrnam",
    "getgrgid",
    "gethostname",
    "sethostname",
    "getdomainname",
    "setdomainname",
    "uname",
    "sysinfo",
    "getrusage",
    "getrusage_children",
    "getrusage_thread",
    "times",
    "clock",
    "clock_gettime",
    "clock_settime",
    "clock_getres",
    "clock_adjtime",
    "nanosleep",
    "usleep",
    "sleep",
    "alarm",
    "setitimer",
    "getitimer",
    "timer_create",
    "timer_delete",
    "timer_settime",
    "timer_gettime",
    "timer_getoverrun",
    "signal",
    "sigaction",
    "sigprocmask",
    "sigpending",
    "sigsuspend",
    "sigwait",
    "sigwaitinfo",
    "sigtimedwait",
    "sigqueue",
    "sigkill",
    "sigstop",
    "sigcont",
    "sigint",
    "sigterm",
    "sigabrt",
    "sigsegv",
    "sigfpe",
    "sigill",
    "sigbus",
    "sigpipe",
    "sigalrm",
    "sigchld",
    "sighup",
    "sigquit",
    "sigtrap",
    "sigsys",
    "sigurg",
    "sigxcpu",
    "sigxfsz",
    "sigvtalrm",
    "sigprof",
    "sigwinch",
    "sigio",
    "sigpoll",
    "sigpwr",
    "sigunused",
    "sigrtmin",
    "sigrtmax",
    "sigemptyset",
    "sigfillset",
    "sigaddset",
    "sigdelset",
    "sigismember",
    "sigsetops",
    "pause",
    "kill",
    "killpg",
    "raise",
    "sigsetjmp",
    "siglongjmp",
    "setjmp",
    "longjmp",
    "__builtin_setjmp",
    "__builtin_longjmp",
    "__builtin_return_address",
    "__builtin_frame_address",
    "__builtin_expect",
    "__builtin_expect_with_probability",
    "__builtin_unreachable",
    "__builtin_trap",
    "__builtin_abort",
    "__builtin_assume",
    "__builtin_assume_aligned",
    "__builtin_prefetch",
    "__builtin_clz",
    "__builtin_ctz",
    "__builtin_popcount",
    "__builtin_parity",
    "__builtin_ffs",
    "__builtin_bswap",
    "__builtin_bswap16",
    "__builtin_bswap32",
    "__builtin_bswap64",
    "__builtin_byteorder",
    "__builtin_endian",
    "__builtin_ntohs",
    "__builtin_htons",
    "__builtin_ntohl",
    "__builtin_htonl",
    "__builtin_constant_p",
    "__builtin_choose_expr",
    "__builtin_types_compatible_p",
    "__builtin_is_constant",
    "__builtin_has_attribute",
    "__builtin_has_feature",
    "__builtin_has_include",
    "__builtin_has_extension",
    "__builtin_has_warning",
    "__builtin_has_declspec",
    "__builtin_has_cpp_attribute",
    "__builtin_LINE",
    "__builtin_FILE",
    "__builtin_FUNCTION",
    "__builtin_FUNC",
    "__builtin_PRETTY_FUNCTION",
    "__builtin_COLUMN",
    "__builtin_compiler",
    "__builtin_version",
    "__builtin_timestamp",
    "__builtin_date",
    "__builtin_time",
    "__builtin_STDC_HOSTED",
    "__builtin_STDC_VERSION",
    "__builtin_STDC_UTF_16",
    "__builtin_STDC_UTF_32",
    "__builtin_STDC_NO_ATOMICS",
    "__builtin_STDC_NO_COMPLEX",
    "__builtin_STDC_NO_THREADS",
    "__builtin_STDC_NO_VLA",
    "__builtin_STDC_IEC_559",
    "__builtin_STDC_IEC_559_COMPLEX",
    "__builtin_STDC_ISO_10646",
    "__builtin_STDC_LIB_EXT1",
    "__builtin_STDC_ANALYZABLE",
    "__builtin_STDC_WANT_LIB_EXT1",
    "__builtin_STDC_MATH_H",
    "__builtin_STDC_MATH_ERRNO",
    "__builtin_STDC_MATH_ERREXCEPT",
    "__builtin_STDC_MATH_FENV_ACCESS",
    "__builtin_STDC_MATH_FAST_MATH",
    "__builtin_STDC_MATH_FINITE_MATH_ONLY",
    "__builtin_STDC_MATH_CONTRACT",
    "__builtin_STDC_MATH_EVAL_METHOD",
    "__builtin_STDC_MATH_FENV_ROUND",
    "__builtin_STDC_MATH_FENV_TRAPS",
    "__builtin_STDC_MATH_FENV_DETERM",
    "__builtin_STDC_MATH_FENV_CX_LIMITED_RANGE",
    "__builtin_STDC_MATH_FENV_CX_FINITE_MATH_ONLY",
    "__builtin_STDC_MATH_FENV_CX_CONTRACT",
    "__builtin_STDC_MATH_FENV_CX_EVAL_METHOD",
    "__builtin_STDC_MATH_FENV_CX_FENV_ROUND",
    "__builtin_STDC_MATH_FENV_CX_FENV_TRAPS",
    "__builtin_STDC_MATH_FENV_CX_FENV_DETERM",
    "__builtin_STDC_MATH_FENV_CX_CX_LIMITED_RANGE",
    "__builtin_STDC_MATH_FENV_CX_CX_FINITE_MATH_ONLY",
};

const char* token_type_name(TokenType type) {
    if (type < 0 || type >= TOKEN_COUNT) return "UNKNOWN";
    return token_names[type];
}

const char* token_type_description(TokenType type) {
    if (type < 0 || type >= TOKEN_COUNT) return "Unknown token";
    return token_descriptions[type];
}

/* 处理 文件结束 */
static Token lexer_handle_eof(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_EOF;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 标识符 */
static Token lexer_handle_ident(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_IDENT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 整数 */
static Token lexer_handle_int(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_INT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 浮点数 */
static Token lexer_handle_float(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_FLOAT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 字符串 */
static Token lexer_handle_string(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_STRING;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 字符 */
static Token lexer_handle_char(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_CHAR;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 布尔 */
static Token lexer_handle_bool(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_BOOL;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 空值 */
static Token lexer_handle_null(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_NULL;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 + */
static Token lexer_handle_plus(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_PLUS;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 - */
static Token lexer_handle_minus(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_MINUS;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 * */
static Token lexer_handle_star(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_STAR;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 / */
static Token lexer_handle_slash(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_SLASH;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 % */
static Token lexer_handle_percent(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_PERCENT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 & */
static Token lexer_handle_amp(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_AMP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 | */
static Token lexer_handle_pipe(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_PIPE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 ^ */
static Token lexer_handle_caret(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_CARET;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 ~ */
static Token lexer_handle_tilde(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_TILDE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 ! */
static Token lexer_handle_bang(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_BANG;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 = */
static Token lexer_handle_eq(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_EQ;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 < */
static Token lexer_handle_lt(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_LT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 > */
static Token lexer_handle_gt(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_GT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 += */
static Token lexer_handle_plus_eq(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_PLUS_EQ;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 -= */
static Token lexer_handle_minus_eq(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_MINUS_EQ;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 *= */
static Token lexer_handle_star_eq(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_STAR_EQ;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 /= */
static Token lexer_handle_slash_eq(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_SLASH_EQ;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 %= */
static Token lexer_handle_percent_eq(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_PERCENT_EQ;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 &= */
static Token lexer_handle_amp_eq(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_AMP_EQ;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 |= */
static Token lexer_handle_pipe_eq(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_PIPE_EQ;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 ^= */
static Token lexer_handle_caret_eq(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_CARET_EQ;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 == */
static Token lexer_handle_eq_eq(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_EQ_EQ;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 != */
static Token lexer_handle_bang_eq(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_BANG_EQ;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 <= */
static Token lexer_handle_lt_eq(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_LT_EQ;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 >= */
static Token lexer_handle_gt_eq(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_GT_EQ;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 && */
static Token lexer_handle_amp_amp(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_AMP_AMP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 || */
static Token lexer_handle_pipe_pipe(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_PIPE_PIPE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 << */
static Token lexer_handle_lt_lt(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_LT_LT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 >> */
static Token lexer_handle_gt_gt(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_GT_GT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 ( */
static Token lexer_handle_lparen(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_LPAREN;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 ) */
static Token lexer_handle_rparen(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_RPAREN;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 { */
static Token lexer_handle_lbrace(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_LBRACE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 } */
static Token lexer_handle_rbrace(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_RBRACE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 [ */
static Token lexer_handle_lbracket(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_LBRACKET;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 ] */
static Token lexer_handle_rbracket(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_RBRACKET;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 , */
static Token lexer_handle_comma(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_COMMA;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 ; */
static Token lexer_handle_semicolon(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_SEMICOLON;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 : */
static Token lexer_handle_colon(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_COLON;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 . */
static Token lexer_handle_dot(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_DOT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 .. */
static Token lexer_handle_dot_dot(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_DOT_DOT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 -> */
static Token lexer_handle_arrow(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_ARROW;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 => */
static Token lexer_handle_fat_arrow(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_FAT_ARROW;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 ? */
static Token lexer_handle_question(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_QUESTION;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 # */
static Token lexer_handle_hash(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_HASH;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 @ */
static Token lexer_handle_at(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_AT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 $ */
static Token lexer_handle_dollar(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_DOLLAR;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 ` */
static Token lexer_handle_backtick(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_BACKTICK;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 \ */
static Token lexer_handle_backslash(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_BACKSLASH;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 let */
static Token lexer_handle_kw_let(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_LET;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 mut */
static Token lexer_handle_kw_mut(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_MUT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 const */
static Token lexer_handle_kw_const(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_CONST;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 fn */
static Token lexer_handle_kw_fn(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_FN;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 return */
static Token lexer_handle_kw_return(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_RETURN;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 if */
static Token lexer_handle_kw_if(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_IF;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 else */
static Token lexer_handle_kw_else(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_ELSE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 while */
static Token lexer_handle_kw_while(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_WHILE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 for */
static Token lexer_handle_kw_for(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_FOR;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 loop */
static Token lexer_handle_kw_loop(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_LOOP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 break */
static Token lexer_handle_kw_break(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_BREAK;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 continue */
static Token lexer_handle_kw_continue(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_CONTINUE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 struct */
static Token lexer_handle_kw_struct(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_STRUCT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 enum */
static Token lexer_handle_kw_enum(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_ENUM;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 trait */
static Token lexer_handle_kw_trait(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_TRAIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 impl */
static Token lexer_handle_kw_impl(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_IMPL;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 use */
static Token lexer_handle_kw_use(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_USE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 mod */
static Token lexer_handle_kw_mod(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_MOD;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 pub */
static Token lexer_handle_kw_pub(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_PUB;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 priv */
static Token lexer_handle_kw_priv(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_PRIV;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 self */
static Token lexer_handle_kw_self(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SELF;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 super */
static Token lexer_handle_kw_super(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SUPER;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 crate */
static Token lexer_handle_kw_crate(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_CRATE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 in */
static Token lexer_handle_kw_in(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_IN;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 as */
static Token lexer_handle_kw_as(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_AS;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 match */
static Token lexer_handle_kw_match(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_MATCH;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 where */
static Token lexer_handle_kw_where(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_WHERE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 type */
static Token lexer_handle_kw_type(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_TYPE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 typeof */
static Token lexer_handle_kw_typeof(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_TYPEOF;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sizeof */
static Token lexer_handle_kw_sizeof(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIZEOF;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 alignof */
static Token lexer_handle_kw_alignof(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_ALIGNOF;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 unsafe */
static Token lexer_handle_kw_unsafe(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_UNSAFE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 extern */
static Token lexer_handle_kw_extern(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_EXTERN;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 native */
static Token lexer_handle_kw_native(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_NATIVE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 import */
static Token lexer_handle_kw_import(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_IMPORT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 export */
static Token lexer_handle_kw_export(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_EXPORT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 from */
static Token lexer_handle_kw_from(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_FROM;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 default */
static Token lexer_handle_kw_default(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_DEFAULT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 static */
static Token lexer_handle_kw_static(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_STATIC;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 volatile */
static Token lexer_handle_kw_volatile(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_VOLATILE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 inline */
static Token lexer_handle_kw_inline(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_INLINE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 noinline */
static Token lexer_handle_kw_noinline(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_NOINLINE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 cold */
static Token lexer_handle_kw_cold(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_COLD;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 hot */
static Token lexer_handle_kw_hot(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_HOT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 pure */
static Token lexer_handle_kw_pure(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_PURE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 impure */
static Token lexer_handle_kw_impure(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_IMPURE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 nonnull */
static Token lexer_handle_kw_nonnull(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_NONNULL;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 nullable */
static Token lexer_handle_kw_nullable(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_NULLABLE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 move */
static Token lexer_handle_kw_move(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_MOVE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 copy */
static Token lexer_handle_kw_copy(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_COPY;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 clone */
static Token lexer_handle_kw_clone(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_CLONE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 drop */
static Token lexer_handle_kw_drop(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_DROP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 new */
static Token lexer_handle_kw_new(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_NEW;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 delete */
static Token lexer_handle_kw_delete(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_DELETE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 malloc */
static Token lexer_handle_kw_malloc(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_MALLOC;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 free */
static Token lexer_handle_kw_free(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_FREE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 alloc */
static Token lexer_handle_kw_alloc(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_ALLOC;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 dealloc */
static Token lexer_handle_kw_dealloc(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_DEALLOC;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 realloc */
static Token lexer_handle_kw_realloc(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_REALLOC;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 zero */
static Token lexer_handle_kw_zero(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_ZERO;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 uninit */
static Token lexer_handle_kw_uninit(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_UNINIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 assume */
static Token lexer_handle_kw_assume(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_ASSUME;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 unreachable */
static Token lexer_handle_kw_unreachable(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_UNREACHABLE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 abort */
static Token lexer_handle_kw_abort(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_ABORT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 panic */
static Token lexer_handle_kw_panic(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_PANIC;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 unwrap */
static Token lexer_handle_kw_unwrap(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_UNWRAP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 expect */
static Token lexer_handle_kw_expect(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_EXPECT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 try */
static Token lexer_handle_kw_try(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_TRY;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 catch */
static Token lexer_handle_kw_catch(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_CATCH;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 throw */
static Token lexer_handle_kw_throw(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THROW;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 raise */
static Token lexer_handle_kw_raise(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_RAISE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 rescue */
static Token lexer_handle_kw_rescue(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_RESCUE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 ensure */
static Token lexer_handle_kw_ensure(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_ENSURE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 finally */
static Token lexer_handle_kw_finally(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_FINALLY;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 defer */
static Token lexer_handle_kw_defer(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_DEFER;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 yield */
static Token lexer_handle_kw_yield(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_YIELD;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 await */
static Token lexer_handle_kw_await(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_AWAIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 async */
static Token lexer_handle_kw_async(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_ASYNC;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sync */
static Token lexer_handle_kw_sync(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SYNC;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 go */
static Token lexer_handle_kw_go(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_GO;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 spawn */
static Token lexer_handle_kw_spawn(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SPAWN;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 join */
static Token lexer_handle_kw_join(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_JOIN;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 select */
static Token lexer_handle_kw_select(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SELECT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 case */
static Token lexer_handle_kw_case(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_CASE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 switch */
static Token lexer_handle_kw_switch(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SWITCH;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 goto */
static Token lexer_handle_kw_goto(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_GOTO;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 label */
static Token lexer_handle_kw_label(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_LABEL;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 macro */
static Token lexer_handle_kw_macro(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_MACRO;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 quote */
static Token lexer_handle_kw_quote(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_QUOTE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 unquote */
static Token lexer_handle_kw_unquote(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_UNQUOTE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 splice */
static Token lexer_handle_kw_splice(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SPLICE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 eval */
static Token lexer_handle_kw_eval(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_EVAL;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 exec */
static Token lexer_handle_kw_exec(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_EXEC;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 shell */
static Token lexer_handle_kw_shell(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SHELL;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 cmd */
static Token lexer_handle_kw_cmd(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_CMD;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 print */
static Token lexer_handle_kw_print(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_PRINT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 println */
static Token lexer_handle_kw_println(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_PRINTLN;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 eprint */
static Token lexer_handle_kw_eprint(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_EPRINT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 eprintln */
static Token lexer_handle_kw_eprintln(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_EPRINTLN;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 assert */
static Token lexer_handle_kw_assert(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_ASSERT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 debug */
static Token lexer_handle_kw_debug(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_DEBUG;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 trace */
static Token lexer_handle_kw_trace(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_TRACE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 info */
static Token lexer_handle_kw_info(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_INFO;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 warn */
static Token lexer_handle_kw_warn(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_WARN;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 error */
static Token lexer_handle_kw_error(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_ERROR;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 fatal */
static Token lexer_handle_kw_fatal(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_FATAL;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 log */
static Token lexer_handle_kw_log(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_LOG;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 true */
static Token lexer_handle_kw_true(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_TRUE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 false */
static Token lexer_handle_kw_false(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_FALSE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 none */
static Token lexer_handle_kw_none(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_NONE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 nil */
static Token lexer_handle_kw_nil(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_NIL;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 undefined */
static Token lexer_handle_kw_undefined(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_UNDEFINED;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 void */
static Token lexer_handle_kw_void(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_VOID;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 unit */
static Token lexer_handle_kw_unit(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_UNIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 never */
static Token lexer_handle_kw_never(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_NEVER;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 any */
static Token lexer_handle_kw_any(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_ANY;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 unknown */
static Token lexer_handle_kw_unknown(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_UNKNOWN;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 infer */
static Token lexer_handle_kw_infer(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_INFER;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 auto */
static Token lexer_handle_kw_auto(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_AUTO;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 dyn */
static Token lexer_handle_kw_dyn(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_DYN;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 impl trait */
static Token lexer_handle_kw_impl_trait(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_IMPL_TRAIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 dyn trait */
static Token lexer_handle_kw_dyn_trait(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_DYN_TRAIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 generic */
static Token lexer_handle_kw_generic(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_GENERIC;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 template */
static Token lexer_handle_kw_template(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_TEMPLATE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 typename */
static Token lexer_handle_kw_typename(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_TYPENAME;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 class */
static Token lexer_handle_kw_class(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_CLASS;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 object */
static Token lexer_handle_kw_object(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_OBJECT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 interface */
static Token lexer_handle_kw_interface(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_INTERFACE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 protocol */
static Token lexer_handle_kw_protocol(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_PROTOCOL;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 extension */
static Token lexer_handle_kw_extension(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_EXTENSION;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 category */
static Token lexer_handle_kw_category(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_CATEGORY;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 subclass */
static Token lexer_handle_kw_subclass(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SUBCLASS;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 superclass */
static Token lexer_handle_kw_superclass(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SUPERCLASS;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 inherit */
static Token lexer_handle_kw_inherit(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_INHERIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 extends */
static Token lexer_handle_kw_extends(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_EXTENDS;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 implements */
static Token lexer_handle_kw_implements(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_IMPLEMENTS;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 conforms */
static Token lexer_handle_kw_conforms(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_CONFORMS;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 adopts */
static Token lexer_handle_kw_adopts(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_ADOPTS;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 satisfies */
static Token lexer_handle_kw_satisfies(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SATISFIES;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 derives */
static Token lexer_handle_kw_derives(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_DERIVES;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 inherits */
static Token lexer_handle_kw_inherits(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_INHERITS;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 override */
static Token lexer_handle_kw_override(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_OVERRIDE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 virtual */
static Token lexer_handle_kw_virtual(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_VIRTUAL;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 abstract */
static Token lexer_handle_kw_abstract(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_ABSTRACT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 final */
static Token lexer_handle_kw_final(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_FINAL;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sealed */
static Token lexer_handle_kw_sealed(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SEALED;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 open */
static Token lexer_handle_kw_open(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_OPEN;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 closed */
static Token lexer_handle_kw_closed(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_CLOSED;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 internal */
static Token lexer_handle_kw_internal(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_INTERNAL;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 protected */
static Token lexer_handle_kw_protected(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_PROTECTED;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 package */
static Token lexer_handle_kw_package(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_PACKAGE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 fileprivate */
static Token lexer_handle_kw_fileprivate(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_FILEPRIVATE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 private(set) */
static Token lexer_handle_kw_private_set(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_PRIVATE_SET;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 get */
static Token lexer_handle_kw_get(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_GET;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 set */
static Token lexer_handle_kw_set(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SET;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 willSet */
static Token lexer_handle_kw_will_set(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_WILL_SET;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 didSet */
static Token lexer_handle_kw_did_set(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_DID_SET;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 lazy */
static Token lexer_handle_kw_lazy(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_LAZY;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 weak */
static Token lexer_handle_kw_weak(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_WEAK;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 unowned */
static Token lexer_handle_kw_unowned(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_UNOWNED;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 strong */
static Token lexer_handle_kw_strong(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_STRONG;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 retain */
static Token lexer_handle_kw_retain(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_RETAIN;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 release */
static Token lexer_handle_kw_release(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_RELEASE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 autorelease */
static Token lexer_handle_kw_autorelease(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_AUTORELEASE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 dealloc */
static Token lexer_handle_kw_dealloc(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_DEALLOC;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 deinit */
static Token lexer_handle_kw_deinit(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_DEINIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 finalize */
static Token lexer_handle_kw_finalize(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_FINALIZE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 dispose */
static Token lexer_handle_kw_dispose(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_DISPOSE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 close */
static Token lexer_handle_kw_close(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_CLOSE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 open (keyword) */
static Token lexer_handle_kw_open_kw(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_OPEN_KW;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 read */
static Token lexer_handle_kw_read(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_READ;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 write */
static Token lexer_handle_kw_write(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_WRITE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 append */
static Token lexer_handle_kw_append(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_APPEND;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 flush */
static Token lexer_handle_kw_flush(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_FLUSH;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 seek */
static Token lexer_handle_kw_seek(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SEEK;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 tell */
static Token lexer_handle_kw_tell(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_TELL;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 eof */
static Token lexer_handle_kw_eof(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_EOF;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 rewind */
static Token lexer_handle_kw_rewind(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_REWIND;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 truncate */
static Token lexer_handle_kw_truncate(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_TRUNCATE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sync (keyword) */
static Token lexer_handle_kw_sync(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SYNC;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 datasync */
static Token lexer_handle_kw_datasync(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_DATASYNC;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 fsync */
static Token lexer_handle_kw_fsync(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_FSYNC;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 fdatasync */
static Token lexer_handle_kw_fdatasync(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_FDATASYNC;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 msync */
static Token lexer_handle_kw_msync(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_MSYNC;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 mmap */
static Token lexer_handle_kw_mmap(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_MMAP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 munmap */
static Token lexer_handle_kw_munmap(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_MUNMAP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 mprotect */
static Token lexer_handle_kw_mprotect(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_MPROTECT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 mlock */
static Token lexer_handle_kw_mlock(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_MLOCK;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 munlock */
static Token lexer_handle_kw_munlock(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_MUNLOCK;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 madvise */
static Token lexer_handle_kw_madvise(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_MADVISE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 mincore */
static Token lexer_handle_kw_mincore(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_MINCORE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 mremap */
static Token lexer_handle_kw_mremap(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_MREMAP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 mremap_fixed */
static Token lexer_handle_kw_mremap_fixed(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_MREMAP_FIXED;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 mremap_maymove */
static Token lexer_handle_kw_mremap_maymove(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_MREMAP_MAYMOVE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 mremap_dontunmap */
static Token lexer_handle_kw_mremap_dontunmap(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_MREMAP_DONTUNMAP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 shm_open */
static Token lexer_handle_kw_shm_open(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SHM_OPEN;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 shm_unlink */
static Token lexer_handle_kw_shm_unlink(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SHM_UNLINK;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sem_open */
static Token lexer_handle_kw_sem_open(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SEM_OPEN;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sem_close */
static Token lexer_handle_kw_sem_close(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SEM_CLOSE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sem_unlink */
static Token lexer_handle_kw_sem_unlink(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SEM_UNLINK;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sem_wait */
static Token lexer_handle_kw_sem_wait(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SEM_WAIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sem_trywait */
static Token lexer_handle_kw_sem_trywait(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SEM_TRYWAIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sem_post */
static Token lexer_handle_kw_sem_post(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SEM_POST;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sem_getvalue */
static Token lexer_handle_kw_sem_getvalue(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SEM_GETVALUE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sem_init */
static Token lexer_handle_kw_sem_init(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SEM_INIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sem_destroy */
static Token lexer_handle_kw_sem_destroy(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SEM_DESTROY;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 mutex_init */
static Token lexer_handle_kw_mutex_init(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_MUTEX_INIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 mutex_destroy */
static Token lexer_handle_kw_mutex_destroy(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_MUTEX_DESTROY;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 mutex_lock */
static Token lexer_handle_kw_mutex_lock(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_MUTEX_LOCK;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 mutex_trylock */
static Token lexer_handle_kw_mutex_trylock(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_MUTEX_TRYLOCK;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 mutex_unlock */
static Token lexer_handle_kw_mutex_unlock(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_MUTEX_UNLOCK;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 mutex_timedlock */
static Token lexer_handle_kw_mutex_timedlock(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_MUTEX_TIMEDLOCK;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 cond_init */
static Token lexer_handle_kw_cond_init(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_COND_INIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 cond_destroy */
static Token lexer_handle_kw_cond_destroy(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_COND_DESTROY;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 cond_wait */
static Token lexer_handle_kw_cond_wait(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_COND_WAIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 cond_timedwait */
static Token lexer_handle_kw_cond_timedwait(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_COND_TIMEDWAIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 cond_signal */
static Token lexer_handle_kw_cond_signal(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_COND_SIGNAL;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 cond_broadcast */
static Token lexer_handle_kw_cond_broadcast(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_COND_BROADCAST;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 rwlock_init */
static Token lexer_handle_kw_rwlock_init(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_RWLOCK_INIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 rwlock_destroy */
static Token lexer_handle_kw_rwlock_destroy(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_RWLOCK_DESTROY;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 rwlock_rdlock */
static Token lexer_handle_kw_rwlock_rdlock(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_RWLOCK_RDLOCK;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 rwlock_wrlock */
static Token lexer_handle_kw_rwlock_wrlock(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_RWLOCK_WRLOCK;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 rwlock_unlock */
static Token lexer_handle_kw_rwlock_unlock(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_RWLOCK_UNLOCK;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 rwlock_tryrdlock */
static Token lexer_handle_kw_rwlock_tryrdlock(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_RWLOCK_TRYRDLOCK;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 rwlock_trywrlock */
static Token lexer_handle_kw_rwlock_trywrlock(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_RWLOCK_TRYWRLOCK;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 spin_init */
static Token lexer_handle_kw_spin_init(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SPIN_INIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 spin_destroy */
static Token lexer_handle_kw_spin_destroy(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SPIN_DESTROY;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 spin_lock */
static Token lexer_handle_kw_spin_lock(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SPIN_LOCK;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 spin_trylock */
static Token lexer_handle_kw_spin_trylock(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SPIN_TRYLOCK;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 spin_unlock */
static Token lexer_handle_kw_spin_unlock(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SPIN_UNLOCK;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 barrier_init */
static Token lexer_handle_kw_barrier_init(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_BARRIER_INIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 barrier_destroy */
static Token lexer_handle_kw_barrier_destroy(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_BARRIER_DESTROY;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 barrier_wait */
static Token lexer_handle_kw_barrier_wait(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_BARRIER_WAIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 once_init */
static Token lexer_handle_kw_once_init(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_ONCE_INIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 once */
static Token lexer_handle_kw_once(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_ONCE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 cleanup_push */
static Token lexer_handle_kw_cleanup_push(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_CLEANUP_PUSH;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 cleanup_pop */
static Token lexer_handle_kw_cleanup_pop(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_CLEANUP_POP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 key_create */
static Token lexer_handle_kw_key_create(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_KEY_CREATE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 key_delete */
static Token lexer_handle_kw_key_delete(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_KEY_DELETE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 key_setspecific */
static Token lexer_handle_kw_key_setspecific(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_KEY_SETSPECIFIC;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 key_getspecific */
static Token lexer_handle_kw_key_getspecific(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_KEY_GETSPECIFIC;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_create */
static Token lexer_handle_kw_thread_create(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_CREATE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_join */
static Token lexer_handle_kw_thread_join(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_JOIN;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_detach */
static Token lexer_handle_kw_thread_detach(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_DETACH;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_exit */
static Token lexer_handle_kw_thread_exit(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_EXIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_self */
static Token lexer_handle_kw_thread_self(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_SELF;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_equal */
static Token lexer_handle_kw_thread_equal(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_EQUAL;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_yield */
static Token lexer_handle_kw_thread_yield(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_YIELD;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_setconcurrency */
static Token lexer_handle_kw_thread_setconcurrency(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_SETCONCURRENCY;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_getconcurrency */
static Token lexer_handle_kw_thread_getconcurrency(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_GETCONCURRENCY;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_setschedparam */
static Token lexer_handle_kw_thread_setschedparam(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_SETSCHEDPARAM;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_getschedparam */
static Token lexer_handle_kw_thread_getschedparam(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_GETSCHEDPARAM;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_setschedprio */
static Token lexer_handle_kw_thread_setschedprio(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_SETSCHEDPRIO;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_getcpuclockid */
static Token lexer_handle_kw_thread_getcpuclockid(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_GETCPUCLOCKID;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_attr_init */
static Token lexer_handle_kw_thread_attr_init(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_ATTR_INIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_attr_destroy */
static Token lexer_handle_kw_thread_attr_destroy(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_ATTR_DESTROY;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_attr_setdetachstate */
static Token lexer_handle_kw_thread_attr_setdetachstate(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_ATTR_SETDETACHSTATE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_attr_getdetachstate */
static Token lexer_handle_kw_thread_attr_getdetachstate(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_ATTR_GETDETACHSTATE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_attr_setstacksize */
static Token lexer_handle_kw_thread_attr_setstacksize(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_ATTR_SETSTACKSIZE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_attr_getstacksize */
static Token lexer_handle_kw_thread_attr_getstacksize(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_ATTR_GETSTACKSIZE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_attr_setstack */
static Token lexer_handle_kw_thread_attr_setstack(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_ATTR_SETSTACK;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_attr_getstack */
static Token lexer_handle_kw_thread_attr_getstack(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_ATTR_GETSTACK;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_attr_setguardsize */
static Token lexer_handle_kw_thread_attr_setguardsize(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_ATTR_SETGUARDSIZE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_attr_getguardsize */
static Token lexer_handle_kw_thread_attr_getguardsize(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_ATTR_GETGUARDSIZE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_attr_setscope */
static Token lexer_handle_kw_thread_attr_setscope(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_ATTR_SETSCOPE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_attr_getscope */
static Token lexer_handle_kw_thread_attr_getscope(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_ATTR_GETSCOPE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_attr_setinheritsched */
static Token lexer_handle_kw_thread_attr_setinheritsched(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_ATTR_SETINHERITSCHED;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_attr_getinheritsched */
static Token lexer_handle_kw_thread_attr_getinheritsched(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_ATTR_GETINHERITSCHED;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_attr_setschedpolicy */
static Token lexer_handle_kw_thread_attr_setschedpolicy(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_ATTR_SETSCHEDPOLICY;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_attr_getschedpolicy */
static Token lexer_handle_kw_thread_attr_getschedpolicy(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_ATTR_GETSCHEDPOLICY;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_attr_setschedparam */
static Token lexer_handle_kw_thread_attr_setschedparam(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_ATTR_SETSCHEDPARAM;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_attr_getschedparam */
static Token lexer_handle_kw_thread_attr_getschedparam(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_ATTR_GETSCHEDPARAM;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_attr_setaffinity_np */
static Token lexer_handle_kw_thread_attr_setaffinity_np(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_ATTR_SETAFFINITY_NP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_attr_getaffinity_np */
static Token lexer_handle_kw_thread_attr_getaffinity_np(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_ATTR_GETAFFINITY_NP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_setaffinity_np */
static Token lexer_handle_kw_thread_setaffinity_np(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_SETAFFINITY_NP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_getaffinity_np */
static Token lexer_handle_kw_thread_getaffinity_np(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_GETAFFINITY_NP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_attr_setname_np */
static Token lexer_handle_kw_thread_attr_setname_np(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_ATTR_SETNAME_NP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_attr_getname_np */
static Token lexer_handle_kw_thread_attr_getname_np(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_ATTR_GETNAME_NP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_setname_np */
static Token lexer_handle_kw_thread_setname_np(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_SETNAME_NP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_getname_np */
static Token lexer_handle_kw_thread_getname_np(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_GETNAME_NP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_setstackaddr_np */
static Token lexer_handle_kw_thread_setstackaddr_np(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_SETSTACKADDR_NP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_getstackaddr_np */
static Token lexer_handle_kw_thread_getstackaddr_np(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_GETSTACKADDR_NP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_setstacksize_np */
static Token lexer_handle_kw_thread_setstacksize_np(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_SETSTACKSIZE_NP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_getstacksize_np */
static Token lexer_handle_kw_thread_getstacksize_np(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_GETSTACKSIZE_NP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_setcancelstate */
static Token lexer_handle_kw_thread_setcancelstate(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_SETCANCELSTATE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_getcancelstate */
static Token lexer_handle_kw_thread_getcancelstate(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_GETCANCELSTATE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_setcanceltype */
static Token lexer_handle_kw_thread_setcanceltype(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_SETCANCELTYPE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_getcanceltype */
static Token lexer_handle_kw_thread_getcanceltype(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_GETCANCELTYPE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_cancel */
static Token lexer_handle_kw_thread_cancel(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_CANCEL;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_testcancel */
static Token lexer_handle_kw_thread_testcancel(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_TESTCANCEL;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_cleanup_push */
static Token lexer_handle_kw_thread_cleanup_push(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_CLEANUP_PUSH;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_cleanup_pop */
static Token lexer_handle_kw_thread_cleanup_pop(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_CLEANUP_POP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_sigmask */
static Token lexer_handle_kw_thread_sigmask(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_SIGMASK;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_kill */
static Token lexer_handle_kw_thread_kill(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_KILL;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 thread_sigqueue */
static Token lexer_handle_kw_thread_sigqueue(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_THREAD_SIGQUEUE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 pthread_atfork */
static Token lexer_handle_kw_pthread_atfork(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_PTHREAD_ATFORK;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 fork */
static Token lexer_handle_kw_fork(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_FORK;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 exec */
static Token lexer_handle_kw_exec(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_EXEC;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 execl */
static Token lexer_handle_kw_execl(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_EXECL;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 execv */
static Token lexer_handle_kw_execv(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_EXECV;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 execle */
static Token lexer_handle_kw_execle(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_EXECLE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 execve */
static Token lexer_handle_kw_execve(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_EXECVE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 execlp */
static Token lexer_handle_kw_execlp(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_EXECLP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 execvp */
static Token lexer_handle_kw_execvp(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_EXECVP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 execvpe */
static Token lexer_handle_kw_execvpe(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_EXECVPE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 fexecve */
static Token lexer_handle_kw_fexecve(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_FEXECVE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 wait */
static Token lexer_handle_kw_wait(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_WAIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 waitpid */
static Token lexer_handle_kw_waitpid(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_WAITPID;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 waitid */
static Token lexer_handle_kw_waitid(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_WAITID;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 wait3 */
static Token lexer_handle_kw_wait3(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_WAIT3;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 wait4 */
static Token lexer_handle_kw_wait4(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_WAIT4;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 exit */
static Token lexer_handle_kw_exit(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_EXIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 _exit */
static Token lexer_handle_kw__exit(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW__EXIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 _exit_group */
static Token lexer_handle_kw__exitgroup(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW__EXITGROUP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 atexit */
static Token lexer_handle_kw_atexit(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_ATEXIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 on_exit */
static Token lexer_handle_kw_on_exit(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_ON_EXIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 getpid */
static Token lexer_handle_kw_getpid(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_GETPID;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 getppid */
static Token lexer_handle_kw_getppid(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_GETPPID;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 getpgid */
static Token lexer_handle_kw_getpgid(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_GETPGID;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 setpgid */
static Token lexer_handle_kw_setpgid(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SETPGID;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 getpgrp */
static Token lexer_handle_kw_getpgrp(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_GETPGRP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 setpgrp */
static Token lexer_handle_kw_setpgrp(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SETPGRP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 getsid */
static Token lexer_handle_kw_getsid(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_GETSID;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 setsid */
static Token lexer_handle_kw_setsid(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SETSID;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 getuid */
static Token lexer_handle_kw_getuid(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_GETUID;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 seteuid */
static Token lexer_handle_kw_seteuid(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SETEUID;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 geteuid */
static Token lexer_handle_kw_geteuid(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_GETEUID;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 setuid */
static Token lexer_handle_kw_setuid(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SETUID;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 getgid */
static Token lexer_handle_kw_getgid(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_GETGID;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 setegid */
static Token lexer_handle_kw_setegid(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SETEGID;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 getegid */
static Token lexer_handle_kw_getegid(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_GETEGID;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 setgid */
static Token lexer_handle_kw_setgid(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SETGID;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 getgroups */
static Token lexer_handle_kw_getgroups(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_GETGROUPS;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 setgroups */
static Token lexer_handle_kw_setgroups(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SETGROUPS;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 getlogin */
static Token lexer_handle_kw_getlogin(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_GETLOGIN;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 setlogin */
static Token lexer_handle_kw_setlogin(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SETLOGIN;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 getpwnam */
static Token lexer_handle_kw_getpwnam(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_GETPWNAM;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 getpwuid */
static Token lexer_handle_kw_getpwuid(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_GETPWUID;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 getgrnam */
static Token lexer_handle_kw_getgrnam(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_GETGRNAM;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 getgrgid */
static Token lexer_handle_kw_getgrgid(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_GETGRGID;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 gethostname */
static Token lexer_handle_kw_gethostname(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_GETHOSTNAME;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sethostname */
static Token lexer_handle_kw_sethostname(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SETHOSTNAME;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 getdomainname */
static Token lexer_handle_kw_getdomainname(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_GETDOMAINNAME;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 setdomainname */
static Token lexer_handle_kw_setdomainname(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SETDOMAINNAME;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 uname */
static Token lexer_handle_kw_uname(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_UNAME;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sysinfo */
static Token lexer_handle_kw_sysinfo(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SYSINFO;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 getrusage */
static Token lexer_handle_kw_getrusage(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_GETRUSAGE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 getrusage_children */
static Token lexer_handle_kw_getrusage_children(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_GETRUSAGE_CHILDREN;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 getrusage_thread */
static Token lexer_handle_kw_getrusage_thread(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_GETRUSAGE_THREAD;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 times */
static Token lexer_handle_kw_times(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_TIMES;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 clock */
static Token lexer_handle_kw_clock(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_CLOCK;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 clock_gettime */
static Token lexer_handle_kw_clock_gettime(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_CLOCK_GETTIME;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 clock_settime */
static Token lexer_handle_kw_clock_settime(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_CLOCK_SETTIME;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 clock_getres */
static Token lexer_handle_kw_clock_getres(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_CLOCK_GETRES;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 clock_adjtime */
static Token lexer_handle_kw_clock_adjtime(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_CLOCK_ADJTIME;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 nanosleep */
static Token lexer_handle_kw_nanosleep(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_NANOSLEEP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 usleep */
static Token lexer_handle_kw_usleep(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_USLEEP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sleep */
static Token lexer_handle_kw_sleep(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SLEEP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 alarm */
static Token lexer_handle_kw_alarm(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_ALARM;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 setitimer */
static Token lexer_handle_kw_setitimer(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SETITIMER;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 getitimer */
static Token lexer_handle_kw_getitimer(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_GETITIMER;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 timer_create */
static Token lexer_handle_kw_timer_create(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_TIMER_CREATE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 timer_delete */
static Token lexer_handle_kw_timer_delete(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_TIMER_DELETE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 timer_settime */
static Token lexer_handle_kw_timer_settime(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_TIMER_SETTIME;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 timer_gettime */
static Token lexer_handle_kw_timer_gettime(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_TIMER_GETTIME;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 timer_getoverrun */
static Token lexer_handle_kw_timer_getoverrun(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_TIMER_GETOVERRUN;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 signal */
static Token lexer_handle_kw_signal(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGNAL;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigaction */
static Token lexer_handle_kw_sigaction(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGACTION;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigprocmask */
static Token lexer_handle_kw_sigprocmask(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGPROCMASK;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigpending */
static Token lexer_handle_kw_sigpending(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGPENDING;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigsuspend */
static Token lexer_handle_kw_sigsuspend(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGSUSPEND;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigwait */
static Token lexer_handle_kw_sigwait(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGWAIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigwaitinfo */
static Token lexer_handle_kw_sigwaitinfo(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGWAITINFO;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigtimedwait */
static Token lexer_handle_kw_sigtimedwait(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGTIMEDWAIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigqueue */
static Token lexer_handle_kw_sigqueue(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGQUEUE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigkill */
static Token lexer_handle_kw_sigkill(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGKILL;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigstop */
static Token lexer_handle_kw_sigstop(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGSTOP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigcont */
static Token lexer_handle_kw_sigcont(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGCONT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigint */
static Token lexer_handle_kw_sigint(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGINT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigterm */
static Token lexer_handle_kw_sigterm(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGTERM;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigabrt */
static Token lexer_handle_kw_sigabrt(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGABRT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigsegv */
static Token lexer_handle_kw_sigsegv(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGSEGV;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigfpe */
static Token lexer_handle_kw_sigfpe(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGFPE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigill */
static Token lexer_handle_kw_sigill(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGILL;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigbus */
static Token lexer_handle_kw_sigbus(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGBUS;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigpipe */
static Token lexer_handle_kw_sigpipe(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGPIPE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigalrm */
static Token lexer_handle_kw_sigalrm(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGALRM;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigchld */
static Token lexer_handle_kw_sigchld(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGCHLD;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sighup */
static Token lexer_handle_kw_sighup(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGHUP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigquit */
static Token lexer_handle_kw_sigquit(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGQUIT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigtrap */
static Token lexer_handle_kw_sigtrap(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGTRAP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigsys */
static Token lexer_handle_kw_sigsys(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGSYS;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigurg */
static Token lexer_handle_kw_sigurg(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGURG;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigxcpu */
static Token lexer_handle_kw_sigxcpu(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGXCPU;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigxfsz */
static Token lexer_handle_kw_sigxfsz(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGXFSZ;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigvtalrm */
static Token lexer_handle_kw_sigvtalrm(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGVTALRM;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigprof */
static Token lexer_handle_kw_sigprof(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGPROF;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigwinch */
static Token lexer_handle_kw_sigwinch(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGWINCH;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigio */
static Token lexer_handle_kw_sigio(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGIO;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigpoll */
static Token lexer_handle_kw_sigpoll(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGPOLL;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigpwr */
static Token lexer_handle_kw_sigpwr(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGPWR;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigunused */
static Token lexer_handle_kw_sigunused(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGUNUSED;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigrtmin */
static Token lexer_handle_kw_sigrtmin(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGRTMIN;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigrtmax */
static Token lexer_handle_kw_sigrtmax(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGRTMAX;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigemptyset */
static Token lexer_handle_kw_sigemptyset(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGEMPTYSET;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigfillset */
static Token lexer_handle_kw_sigfillset(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGFILLSET;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigaddset */
static Token lexer_handle_kw_sigaddset(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGADDSET;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigdelset */
static Token lexer_handle_kw_sigdelset(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGDELSET;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigismember */
static Token lexer_handle_kw_sigismember(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGISMEMBER;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigsetops */
static Token lexer_handle_kw_sigsetops(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGSETOPS;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 pause */
static Token lexer_handle_kw_pause(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_PAUSE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 kill */
static Token lexer_handle_kw_kill(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_KILL;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 killpg */
static Token lexer_handle_kw_killpg(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_KILLPG;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 raise */
static Token lexer_handle_kw_raise(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_RAISE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 sigsetjmp */
static Token lexer_handle_kw_sigsetjmp(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGSETJMP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 siglongjmp */
static Token lexer_handle_kw_siglongjmp(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SIGLONGJMP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 setjmp */
static Token lexer_handle_kw_setjmp(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_SETJMP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 longjmp */
static Token lexer_handle_kw_longjmp(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW_LONGJMP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_setjmp */
static Token lexer_handle_kw___builtin_setjmp(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_SETJMP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_longjmp */
static Token lexer_handle_kw___builtin_longjmp(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_LONGJMP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_return_address */
static Token lexer_handle_kw___builtin_return_address(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_RETURN_ADDRESS;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_frame_address */
static Token lexer_handle_kw___builtin_frame_address(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_FRAME_ADDRESS;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_expect */
static Token lexer_handle_kw___builtin_expect(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_EXPECT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_expect_with_probability */
static Token lexer_handle_kw___builtin_expect_with_probability(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_EXPECT_WITH_PROBABILITY;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_unreachable */
static Token lexer_handle_kw___builtin_unreachable(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_UNREACHABLE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_trap */
static Token lexer_handle_kw___builtin_trap(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_TRAP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_abort */
static Token lexer_handle_kw___builtin_abort(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_ABORT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_assume */
static Token lexer_handle_kw___builtin_assume(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_ASSUME;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_assume_aligned */
static Token lexer_handle_kw___builtin_assume_aligned(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_ASSUME_ALIGNED;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_prefetch */
static Token lexer_handle_kw___builtin_prefetch(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_PREFETCH;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_clz */
static Token lexer_handle_kw___builtin_clz(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_CLZ;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_ctz */
static Token lexer_handle_kw___builtin_ctz(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_CTZ;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_popcount */
static Token lexer_handle_kw___builtin_popcount(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_POPCOUNT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_parity */
static Token lexer_handle_kw___builtin_parity(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_PARITY;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_ffs */
static Token lexer_handle_kw___builtin_ffs(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_FFS;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_bswap */
static Token lexer_handle_kw___builtin_bswap(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_BSWAP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_bswap16 */
static Token lexer_handle_kw___builtin_bswap16(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_BSWAP16;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_bswap32 */
static Token lexer_handle_kw___builtin_bswap32(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_BSWAP32;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_bswap64 */
static Token lexer_handle_kw___builtin_bswap64(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_BSWAP64;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_byteorder */
static Token lexer_handle_kw___builtin_byteorder(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_BYTEORDER;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_endian */
static Token lexer_handle_kw___builtin_endian(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_ENDIAN;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_ntohs */
static Token lexer_handle_kw___builtin_ntohs(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_NTOHS;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_htons */
static Token lexer_handle_kw___builtin_htons(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_HTONS;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_ntohl */
static Token lexer_handle_kw___builtin_ntohl(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_NTOHL;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_htonl */
static Token lexer_handle_kw___builtin_htonl(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_HTONL;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_constant_p */
static Token lexer_handle_kw___builtin_constant_p(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_CONSTANT_P;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_choose_expr */
static Token lexer_handle_kw___builtin_choose_expr(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_CHOOSE_EXPR;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_types_compatible_p */
static Token lexer_handle_kw___builtin_types_compatible_p(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_TYPES_COMPATIBLE_P;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_is_constant */
static Token lexer_handle_kw___builtin_is_constant(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_IS_CONSTANT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_has_attribute */
static Token lexer_handle_kw___builtin_has_attribute(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_HAS_ATTRIBUTE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_has_feature */
static Token lexer_handle_kw___builtin_has_feature(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_HAS_FEATURE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_has_include */
static Token lexer_handle_kw___builtin_has_include(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_HAS_INCLUDE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_has_extension */
static Token lexer_handle_kw___builtin_has_extension(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_HAS_EXTENSION;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_has_warning */
static Token lexer_handle_kw___builtin_has_warning(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_HAS_WARNING;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_has_declspec */
static Token lexer_handle_kw___builtin_has_declspec(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_HAS_DECLSPEC;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_has_cpp_attribute */
static Token lexer_handle_kw___builtin_has_cpp_attribute(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_HAS_CPP_ATTRIBUTE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_LINE */
static Token lexer_handle_kw___builtin_line(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_LINE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_FILE */
static Token lexer_handle_kw___builtin_file(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_FILE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_FUNCTION */
static Token lexer_handle_kw___builtin_function(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_FUNCTION;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_FUNC */
static Token lexer_handle_kw___builtin_func(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_FUNC;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_PRETTY_FUNCTION */
static Token lexer_handle_kw___builtin_pretty_function(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_PRETTY_FUNCTION;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_COLUMN */
static Token lexer_handle_kw___builtin_column(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_COLUMN;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_compiler */
static Token lexer_handle_kw___builtin_compiler(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_COMPILER;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_version */
static Token lexer_handle_kw___builtin_version(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_VERSION;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_timestamp */
static Token lexer_handle_kw___builtin_timestamp(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_TIMESTAMP;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_date */
static Token lexer_handle_kw___builtin_date(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_DATE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_time */
static Token lexer_handle_kw___builtin_time(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_TIME;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_HOSTED */
static Token lexer_handle_kw___builtin_stdc_hosted(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_HOSTED;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_VERSION */
static Token lexer_handle_kw___builtin_stdc_version(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_VERSION;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_UTF_16 */
static Token lexer_handle_kw___builtin_stdc_utf_16(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_UTF_16;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_UTF_32 */
static Token lexer_handle_kw___builtin_stdc_utf_32(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_UTF_32;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_NO_ATOMICS */
static Token lexer_handle_kw___builtin_stdc_no_atomics(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_NO_ATOMICS;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_NO_COMPLEX */
static Token lexer_handle_kw___builtin_stdc_no_complex(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_NO_COMPLEX;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_NO_THREADS */
static Token lexer_handle_kw___builtin_stdc_no_threads(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_NO_THREADS;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_NO_VLA */
static Token lexer_handle_kw___builtin_stdc_no_vla(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_NO_VLA;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_IEC_559 */
static Token lexer_handle_kw___builtin_stdc_iec_559(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_IEC_559;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_IEC_559_COMPLEX */
static Token lexer_handle_kw___builtin_stdc_iec_559_complex(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_IEC_559_COMPLEX;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_ISO_10646 */
static Token lexer_handle_kw___builtin_stdc_iso_10646(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_ISO_10646;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_LIB_EXT1 */
static Token lexer_handle_kw___builtin_stdc_lib_ext1(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_LIB_EXT1;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_ANALYZABLE */
static Token lexer_handle_kw___builtin_stdc_analyzable(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_ANALYZABLE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_WANT_LIB_EXT1 */
static Token lexer_handle_kw___builtin_stdc_want_lib_ext1(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_WANT_LIB_EXT1;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_MATH_H */
static Token lexer_handle_kw___builtin_stdc_math_h(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_MATH_H;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_MATH_ERRNO */
static Token lexer_handle_kw___builtin_stdc_math_errno(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_MATH_ERRNO;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_MATH_ERREXCEPT */
static Token lexer_handle_kw___builtin_stdc_math_errexcept(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_MATH_ERREXCEPT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_MATH_FENV_ACCESS */
static Token lexer_handle_kw___builtin_stdc_math_fenv_access(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_MATH_FENV_ACCESS;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_MATH_FAST_MATH */
static Token lexer_handle_kw___builtin_stdc_math_fast_math(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_MATH_FAST_MATH;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_MATH_FINITE_MATH_ONLY */
static Token lexer_handle_kw___builtin_stdc_math_finite_math_only(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_MATH_FINITE_MATH_ONLY;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_MATH_CONTRACT */
static Token lexer_handle_kw___builtin_stdc_math_contract(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_MATH_CONTRACT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_MATH_EVAL_METHOD */
static Token lexer_handle_kw___builtin_stdc_math_eval_method(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_MATH_EVAL_METHOD;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_MATH_FENV_ROUND */
static Token lexer_handle_kw___builtin_stdc_math_fenv_round(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_MATH_FENV_ROUND;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_MATH_FENV_TRAPS */
static Token lexer_handle_kw___builtin_stdc_math_fenv_traps(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_MATH_FENV_TRAPS;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_MATH_FENV_DETERM */
static Token lexer_handle_kw___builtin_stdc_math_fenv_determ(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_MATH_FENV_DETERM;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_MATH_FENV_CX_LIMITED_RANGE */
static Token lexer_handle_kw___builtin_stdc_math_fenv_cx_limited_range(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_MATH_FENV_CX_LIMITED_RANGE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_MATH_FENV_CX_FINITE_MATH_ONLY */
static Token lexer_handle_kw___builtin_stdc_math_fenv_cx_finite_math_only(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_MATH_FENV_CX_FINITE_MATH_ONLY;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_MATH_FENV_CX_CONTRACT */
static Token lexer_handle_kw___builtin_stdc_math_fenv_cx_contract(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_MATH_FENV_CX_CONTRACT;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_MATH_FENV_CX_EVAL_METHOD */
static Token lexer_handle_kw___builtin_stdc_math_fenv_cx_eval_method(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_MATH_FENV_CX_EVAL_METHOD;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_MATH_FENV_CX_FENV_ROUND */
static Token lexer_handle_kw___builtin_stdc_math_fenv_cx_fenv_round(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_MATH_FENV_CX_FENV_ROUND;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_MATH_FENV_CX_FENV_TRAPS */
static Token lexer_handle_kw___builtin_stdc_math_fenv_cx_fenv_traps(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_MATH_FENV_CX_FENV_TRAPS;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_MATH_FENV_CX_FENV_DETERM */
static Token lexer_handle_kw___builtin_stdc_math_fenv_cx_fenv_determ(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_MATH_FENV_CX_FENV_DETERM;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_MATH_FENV_CX_CX_LIMITED_RANGE */
static Token lexer_handle_kw___builtin_stdc_math_fenv_cx_cx_limited_range(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_MATH_FENV_CX_CX_LIMITED_RANGE;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}

/* 处理 __builtin_STDC_MATH_FENV_CX_CX_FINITE_MATH_ONLY */
static Token lexer_handle_kw___builtin_stdc_math_fenv_cx_cx_finite_math_only(Lexer* lexer) {
    Token tok;
    tok.type = TOKEN_KW___BUILTIN_STDC_MATH_FENV_CX_CX_FINITE_MATH_ONLY;
    tok.line = lexer->line;
    tok.col = lexer->col;
    tok.pos = lexer->pos;
    tok.value = NULL;
    tok.length = 1;
    lexer->pos++;
    lexer->col++;
    return tok;
}
