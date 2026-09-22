/*
 * Aurora 编译器前端 - 词法分析器
 * 支持 600+ Token 类型
 */

#ifndef AURORA_LEXER_H
#define AURORA_LEXER_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

/* Token 类型枚举 */
typedef enum {
    TOKEN_EOF = 0, /* 文件结束 */
    TOKEN_IDENT = 1, /* 标识符 */
    TOKEN_INT = 2, /* 整数 */
    TOKEN_FLOAT = 3, /* 浮点数 */
    TOKEN_STRING = 4, /* 字符串 */
    TOKEN_CHAR = 5, /* 字符 */
    TOKEN_BOOL = 6, /* 布尔 */
    TOKEN_NULL = 7, /* 空值 */
    TOKEN_PLUS = 10, /* + */
    TOKEN_MINUS = 11, /* - */
    TOKEN_STAR = 12, /* * */
    TOKEN_SLASH = 13, /* / */
    TOKEN_PERCENT = 14, /* % */
    TOKEN_AMP = 15, /* & */
    TOKEN_PIPE = 16, /* | */
    TOKEN_CARET = 17, /* ^ */
    TOKEN_TILDE = 18, /* ~ */
    TOKEN_BANG = 19, /* ! */
    TOKEN_EQ = 20, /* = */
    TOKEN_LT = 21, /* < */
    TOKEN_GT = 22, /* > */
    TOKEN_PLUS_EQ = 23, /* += */
    TOKEN_MINUS_EQ = 24, /* -= */
    TOKEN_STAR_EQ = 25, /* *= */
    TOKEN_SLASH_EQ = 26, /* /= */
    TOKEN_PERCENT_EQ = 27, /* %= */
    TOKEN_AMP_EQ = 28, /* &= */
    TOKEN_PIPE_EQ = 29, /* |= */
    TOKEN_CARET_EQ = 30, /* ^= */
    TOKEN_EQ_EQ = 31, /* == */
    TOKEN_BANG_EQ = 32, /* != */
    TOKEN_LT_EQ = 33, /* <= */
    TOKEN_GT_EQ = 34, /* >= */
    TOKEN_AMP_AMP = 35, /* && */
    TOKEN_PIPE_PIPE = 36, /* || */
    TOKEN_LT_LT = 37, /* << */
    TOKEN_GT_GT = 38, /* >> */
    TOKEN_LPAREN = 40, /* ( */
    TOKEN_RPAREN = 41, /* ) */
    TOKEN_LBRACE = 42, /* { */
    TOKEN_RBRACE = 43, /* } */
    TOKEN_LBRACKET = 44, /* [ */
    TOKEN_RBRACKET = 45, /* ] */
    TOKEN_COMMA = 46, /* , */
    TOKEN_SEMICOLON = 47, /* ; */
    TOKEN_COLON = 48, /* : */
    TOKEN_DOT = 49, /* . */
    TOKEN_DOT_DOT = 50, /* .. */
    TOKEN_ARROW = 51, /* -> */
    TOKEN_FAT_ARROW = 52, /* => */
    TOKEN_QUESTION = 53, /* ? */
    TOKEN_HASH = 54, /* # */
    TOKEN_AT = 55, /* @ */
    TOKEN_DOLLAR = 56, /* $ */
    TOKEN_BACKTICK = 57, /* ` */
    TOKEN_BACKSLASH = 58, /* \ */
    TOKEN_KW_LET = 100, /* let */
    TOKEN_KW_MUT = 101, /* mut */
    TOKEN_KW_CONST = 102, /* const */
    TOKEN_KW_FN = 103, /* fn */
    TOKEN_KW_RETURN = 104, /* return */
    TOKEN_KW_IF = 105, /* if */
    TOKEN_KW_ELSE = 106, /* else */
    TOKEN_KW_WHILE = 107, /* while */
    TOKEN_KW_FOR = 108, /* for */
    TOKEN_KW_LOOP = 109, /* loop */
    TOKEN_KW_BREAK = 110, /* break */
    TOKEN_KW_CONTINUE = 111, /* continue */
    TOKEN_KW_STRUCT = 112, /* struct */
    TOKEN_KW_ENUM = 113, /* enum */
    TOKEN_KW_TRAIT = 114, /* trait */
    TOKEN_KW_IMPL = 115, /* impl */
    TOKEN_KW_USE = 116, /* use */
    TOKEN_KW_MOD = 117, /* mod */
    TOKEN_KW_PUB = 118, /* pub */
    TOKEN_KW_PRIV = 119, /* priv */
    TOKEN_KW_SELF = 120, /* self */
    TOKEN_KW_SUPER = 121, /* super */
    TOKEN_KW_CRATE = 122, /* crate */
    TOKEN_KW_IN = 123, /* in */
    TOKEN_KW_AS = 124, /* as */
    TOKEN_KW_MATCH = 125, /* match */
    TOKEN_KW_WHERE = 126, /* where */
    TOKEN_KW_TYPE = 127, /* type */
    TOKEN_KW_TYPEOF = 128, /* typeof */
    TOKEN_KW_SIZEOF = 129, /* sizeof */
    TOKEN_KW_ALIGNOF = 130, /* alignof */
    TOKEN_KW_UNSAFE = 131, /* unsafe */
    TOKEN_KW_EXTERN = 132, /* extern */
    TOKEN_KW_NATIVE = 133, /* native */
    TOKEN_KW_IMPORT = 134, /* import */
    TOKEN_KW_EXPORT = 135, /* export */
    TOKEN_KW_FROM = 136, /* from */
    TOKEN_KW_DEFAULT = 137, /* default */
    TOKEN_KW_STATIC = 138, /* static */
    TOKEN_KW_VOLATILE = 139, /* volatile */
    TOKEN_KW_INLINE = 140, /* inline */
    TOKEN_KW_NOINLINE = 141, /* noinline */
    TOKEN_KW_COLD = 142, /* cold */
    TOKEN_KW_HOT = 143, /* hot */
    TOKEN_KW_PURE = 144, /* pure */
    TOKEN_KW_IMPURE = 145, /* impure */
    TOKEN_KW_NONNULL = 146, /* nonnull */
    TOKEN_KW_NULLABLE = 147, /* nullable */
    TOKEN_KW_MOVE = 148, /* move */
    TOKEN_KW_COPY = 149, /* copy */
    TOKEN_KW_CLONE = 150, /* clone */
    TOKEN_KW_DROP = 151, /* drop */
    TOKEN_KW_NEW = 152, /* new */
    TOKEN_KW_DELETE = 153, /* delete */
    TOKEN_KW_MALLOC = 154, /* malloc */
    TOKEN_KW_FREE = 155, /* free */
    TOKEN_KW_ALLOC = 156, /* alloc */
    TOKEN_KW_DEALLOC = 157, /* dealloc */
    TOKEN_KW_REALLOC = 158, /* realloc */
    TOKEN_KW_ZERO = 159, /* zero */
    TOKEN_KW_UNINIT = 160, /* uninit */
    TOKEN_KW_ASSUME = 161, /* assume */
    TOKEN_KW_UNREACHABLE = 162, /* unreachable */
    TOKEN_KW_ABORT = 163, /* abort */
    TOKEN_KW_PANIC = 164, /* panic */
    TOKEN_KW_UNWRAP = 165, /* unwrap */
    TOKEN_KW_EXPECT = 166, /* expect */
    TOKEN_KW_TRY = 167, /* try */
    TOKEN_KW_CATCH = 168, /* catch */
    TOKEN_KW_THROW = 169, /* throw */
    TOKEN_KW_RAISE = 170, /* raise */
    TOKEN_KW_RESCUE = 171, /* rescue */
    TOKEN_KW_ENSURE = 172, /* ensure */
    TOKEN_KW_FINALLY = 173, /* finally */
    TOKEN_KW_DEFER = 174, /* defer */
    TOKEN_KW_YIELD = 175, /* yield */
    TOKEN_KW_AWAIT = 176, /* await */
    TOKEN_KW_ASYNC = 177, /* async */
    TOKEN_KW_SYNC = 178, /* sync */
    TOKEN_KW_GO = 179, /* go */
    TOKEN_KW_SPAWN = 180, /* spawn */
    TOKEN_KW_JOIN = 181, /* join */
    TOKEN_KW_SELECT = 182, /* select */
    TOKEN_KW_CASE = 183, /* case */
    TOKEN_KW_SWITCH = 184, /* switch */
    TOKEN_KW_GOTO = 185, /* goto */
    TOKEN_KW_LABEL = 186, /* label */
    TOKEN_KW_MACRO = 187, /* macro */
    TOKEN_KW_QUOTE = 188, /* quote */
    TOKEN_KW_UNQUOTE = 189, /* unquote */
    TOKEN_KW_SPLICE = 190, /* splice */
    TOKEN_KW_EVAL = 191, /* eval */
    TOKEN_KW_EXEC = 192, /* exec */
    TOKEN_KW_SHELL = 193, /* shell */
    TOKEN_KW_CMD = 194, /* cmd */
    TOKEN_KW_PRINT = 195, /* print */
    TOKEN_KW_PRINTLN = 196, /* println */
    TOKEN_KW_EPRINT = 197, /* eprint */
    TOKEN_KW_EPRINTLN = 198, /* eprintln */
    TOKEN_KW_ASSERT = 199, /* assert */
    TOKEN_KW_DEBUG = 200, /* debug */
    TOKEN_KW_TRACE = 201, /* trace */
    TOKEN_KW_INFO = 202, /* info */
    TOKEN_KW_WARN = 203, /* warn */
    TOKEN_KW_ERROR = 204, /* error */
    TOKEN_KW_FATAL = 205, /* fatal */
    TOKEN_KW_LOG = 206, /* log */
    TOKEN_KW_TRUE = 207, /* true */
    TOKEN_KW_FALSE = 208, /* false */
    TOKEN_KW_NONE = 209, /* none */
    TOKEN_KW_NIL = 210, /* nil */
    TOKEN_KW_UNDEFINED = 211, /* undefined */
    TOKEN_KW_VOID = 212, /* void */
    TOKEN_KW_UNIT = 213, /* unit */
    TOKEN_KW_NEVER = 214, /* never */
    TOKEN_KW_ANY = 215, /* any */
    TOKEN_KW_UNKNOWN = 216, /* unknown */
    TOKEN_KW_INFER = 217, /* infer */
    TOKEN_KW_AUTO = 218, /* auto */
    TOKEN_KW_DYN = 219, /* dyn */
    TOKEN_KW_IMPL_TRAIT = 220, /* impl trait */
    TOKEN_KW_DYN_TRAIT = 221, /* dyn trait */
    TOKEN_KW_GENERIC = 222, /* generic */
    TOKEN_KW_TEMPLATE = 223, /* template */
    TOKEN_KW_TYPENAME = 224, /* typename */
    TOKEN_KW_CLASS = 225, /* class */
    TOKEN_KW_OBJECT = 226, /* object */
    TOKEN_KW_INTERFACE = 227, /* interface */
    TOKEN_KW_PROTOCOL = 228, /* protocol */
    TOKEN_KW_EXTENSION = 229, /* extension */
    TOKEN_KW_CATEGORY = 230, /* category */
    TOKEN_KW_SUBCLASS = 231, /* subclass */
    TOKEN_KW_SUPERCLASS = 232, /* superclass */
    TOKEN_KW_INHERIT = 233, /* inherit */
    TOKEN_KW_EXTENDS = 234, /* extends */
    TOKEN_KW_IMPLEMENTS = 235, /* implements */
    TOKEN_KW_CONFORMS = 236, /* conforms */
    TOKEN_KW_ADOPTS = 237, /* adopts */
    TOKEN_KW_SATISFIES = 238, /* satisfies */
    TOKEN_KW_DERIVES = 239, /* derives */
    TOKEN_KW_INHERITS = 240, /* inherits */
    TOKEN_KW_OVERRIDE = 241, /* override */
    TOKEN_KW_VIRTUAL = 242, /* virtual */
    TOKEN_KW_ABSTRACT = 243, /* abstract */
    TOKEN_KW_FINAL = 244, /* final */
    TOKEN_KW_SEALED = 245, /* sealed */
    TOKEN_KW_OPEN = 246, /* open */
    TOKEN_KW_CLOSED = 247, /* closed */
    TOKEN_KW_INTERNAL = 248, /* internal */
    TOKEN_KW_PROTECTED = 249, /* protected */
    TOKEN_KW_PACKAGE = 250, /* package */
    TOKEN_KW_FILEPRIVATE = 251, /* fileprivate */
    TOKEN_KW_PRIVATE_SET = 252, /* private(set) */
    TOKEN_KW_GET = 253, /* get */
    TOKEN_KW_SET = 254, /* set */
    TOKEN_KW_WILL_SET = 255, /* willSet */
    TOKEN_KW_DID_SET = 256, /* didSet */
    TOKEN_KW_LAZY = 257, /* lazy */
    TOKEN_KW_WEAK = 258, /* weak */
    TOKEN_KW_UNOWNED = 259, /* unowned */
    TOKEN_KW_STRONG = 260, /* strong */
    TOKEN_KW_RETAIN = 261, /* retain */
    TOKEN_KW_RELEASE = 262, /* release */
    TOKEN_KW_AUTORELEASE = 263, /* autorelease */
    TOKEN_KW_DEALLOC = 264, /* dealloc */
    TOKEN_KW_DEINIT = 265, /* deinit */
    TOKEN_KW_FINALIZE = 266, /* finalize */
    TOKEN_KW_DISPOSE = 267, /* dispose */
    TOKEN_KW_CLOSE = 268, /* close */
    TOKEN_KW_OPEN_KW = 269, /* open (keyword) */
    TOKEN_KW_READ = 270, /* read */
    TOKEN_KW_WRITE = 271, /* write */
    TOKEN_KW_APPEND = 272, /* append */
    TOKEN_KW_FLUSH = 273, /* flush */
    TOKEN_KW_SEEK = 274, /* seek */
    TOKEN_KW_TELL = 275, /* tell */
    TOKEN_KW_EOF = 276, /* eof */
    TOKEN_KW_REWIND = 277, /* rewind */
    TOKEN_KW_TRUNCATE = 278, /* truncate */
    TOKEN_KW_SYNC = 279, /* sync (keyword) */
    TOKEN_KW_DATASYNC = 280, /* datasync */
    TOKEN_KW_FSYNC = 281, /* fsync */
    TOKEN_KW_FDATASYNC = 282, /* fdatasync */
    TOKEN_KW_MSYNC = 283, /* msync */
    TOKEN_KW_MMAP = 284, /* mmap */
    TOKEN_KW_MUNMAP = 285, /* munmap */
    TOKEN_KW_MPROTECT = 286, /* mprotect */
    TOKEN_KW_MLOCK = 287, /* mlock */
    TOKEN_KW_MUNLOCK = 288, /* munlock */
    TOKEN_KW_MADVISE = 289, /* madvise */
    TOKEN_KW_MINCORE = 290, /* mincore */
    TOKEN_KW_MREMAP = 291, /* mremap */
    TOKEN_KW_MREMAP_FIXED = 292, /* mremap_fixed */
    TOKEN_KW_MREMAP_MAYMOVE = 293, /* mremap_maymove */
    TOKEN_KW_MREMAP_DONTUNMAP = 294, /* mremap_dontunmap */
    TOKEN_KW_SHM_OPEN = 295, /* shm_open */
    TOKEN_KW_SHM_UNLINK = 296, /* shm_unlink */
    TOKEN_KW_SEM_OPEN = 297, /* sem_open */
    TOKEN_KW_SEM_CLOSE = 298, /* sem_close */
    TOKEN_KW_SEM_UNLINK = 299, /* sem_unlink */
    TOKEN_KW_SEM_WAIT = 300, /* sem_wait */
    TOKEN_KW_SEM_TRYWAIT = 301, /* sem_trywait */
    TOKEN_KW_SEM_POST = 302, /* sem_post */
    TOKEN_KW_SEM_GETVALUE = 303, /* sem_getvalue */
    TOKEN_KW_SEM_INIT = 304, /* sem_init */
    TOKEN_KW_SEM_DESTROY = 305, /* sem_destroy */
    TOKEN_KW_MUTEX_INIT = 306, /* mutex_init */
    TOKEN_KW_MUTEX_DESTROY = 307, /* mutex_destroy */
    TOKEN_KW_MUTEX_LOCK = 308, /* mutex_lock */
    TOKEN_KW_MUTEX_TRYLOCK = 309, /* mutex_trylock */
    TOKEN_KW_MUTEX_UNLOCK = 310, /* mutex_unlock */
    TOKEN_KW_MUTEX_TIMEDLOCK = 311, /* mutex_timedlock */
    TOKEN_KW_COND_INIT = 312, /* cond_init */
    TOKEN_KW_COND_DESTROY = 313, /* cond_destroy */
    TOKEN_KW_COND_WAIT = 314, /* cond_wait */
    TOKEN_KW_COND_TIMEDWAIT = 315, /* cond_timedwait */
    TOKEN_KW_COND_SIGNAL = 316, /* cond_signal */
    TOKEN_KW_COND_BROADCAST = 317, /* cond_broadcast */
    TOKEN_KW_RWLOCK_INIT = 318, /* rwlock_init */
    TOKEN_KW_RWLOCK_DESTROY = 319, /* rwlock_destroy */
    TOKEN_KW_RWLOCK_RDLOCK = 320, /* rwlock_rdlock */
    TOKEN_KW_RWLOCK_WRLOCK = 321, /* rwlock_wrlock */
    TOKEN_KW_RWLOCK_UNLOCK = 322, /* rwlock_unlock */
    TOKEN_KW_RWLOCK_TRYRDLOCK = 323, /* rwlock_tryrdlock */
    TOKEN_KW_RWLOCK_TRYWRLOCK = 324, /* rwlock_trywrlock */
    TOKEN_KW_SPIN_INIT = 325, /* spin_init */
    TOKEN_KW_SPIN_DESTROY = 326, /* spin_destroy */
    TOKEN_KW_SPIN_LOCK = 327, /* spin_lock */
    TOKEN_KW_SPIN_TRYLOCK = 328, /* spin_trylock */
    TOKEN_KW_SPIN_UNLOCK = 329, /* spin_unlock */
    TOKEN_KW_BARRIER_INIT = 330, /* barrier_init */
    TOKEN_KW_BARRIER_DESTROY = 331, /* barrier_destroy */
    TOKEN_KW_BARRIER_WAIT = 332, /* barrier_wait */
    TOKEN_KW_ONCE_INIT = 333, /* once_init */
    TOKEN_KW_ONCE = 334, /* once */
    TOKEN_KW_CLEANUP_PUSH = 335, /* cleanup_push */
    TOKEN_KW_CLEANUP_POP = 336, /* cleanup_pop */
    TOKEN_KW_KEY_CREATE = 337, /* key_create */
    TOKEN_KW_KEY_DELETE = 338, /* key_delete */
    TOKEN_KW_KEY_SETSPECIFIC = 339, /* key_setspecific */
    TOKEN_KW_KEY_GETSPECIFIC = 340, /* key_getspecific */
    TOKEN_KW_THREAD_CREATE = 341, /* thread_create */
    TOKEN_KW_THREAD_JOIN = 342, /* thread_join */
    TOKEN_KW_THREAD_DETACH = 343, /* thread_detach */
    TOKEN_KW_THREAD_EXIT = 344, /* thread_exit */
    TOKEN_KW_THREAD_SELF = 345, /* thread_self */
    TOKEN_KW_THREAD_EQUAL = 346, /* thread_equal */
    TOKEN_KW_THREAD_YIELD = 347, /* thread_yield */
    TOKEN_KW_THREAD_SETCONCURRENCY = 348, /* thread_setconcurrency */
    TOKEN_KW_THREAD_GETCONCURRENCY = 349, /* thread_getconcurrency */
    TOKEN_KW_THREAD_SETSCHEDPARAM = 350, /* thread_setschedparam */
    TOKEN_KW_THREAD_GETSCHEDPARAM = 351, /* thread_getschedparam */
    TOKEN_KW_THREAD_SETSCHEDPRIO = 352, /* thread_setschedprio */
    TOKEN_KW_THREAD_GETCPUCLOCKID = 353, /* thread_getcpuclockid */
    TOKEN_KW_THREAD_ATTR_INIT = 354, /* thread_attr_init */
    TOKEN_KW_THREAD_ATTR_DESTROY = 355, /* thread_attr_destroy */
    TOKEN_KW_THREAD_ATTR_SETDETACHSTATE = 356, /* thread_attr_setdetachstate */
    TOKEN_KW_THREAD_ATTR_GETDETACHSTATE = 357, /* thread_attr_getdetachstate */
    TOKEN_KW_THREAD_ATTR_SETSTACKSIZE = 358, /* thread_attr_setstacksize */
    TOKEN_KW_THREAD_ATTR_GETSTACKSIZE = 359, /* thread_attr_getstacksize */
    TOKEN_KW_THREAD_ATTR_SETSTACK = 360, /* thread_attr_setstack */
    TOKEN_KW_THREAD_ATTR_GETSTACK = 361, /* thread_attr_getstack */
    TOKEN_KW_THREAD_ATTR_SETGUARDSIZE = 362, /* thread_attr_setguardsize */
    TOKEN_KW_THREAD_ATTR_GETGUARDSIZE = 363, /* thread_attr_getguardsize */
    TOKEN_KW_THREAD_ATTR_SETSCOPE = 364, /* thread_attr_setscope */
    TOKEN_KW_THREAD_ATTR_GETSCOPE = 365, /* thread_attr_getscope */
    TOKEN_KW_THREAD_ATTR_SETINHERITSCHED = 366, /* thread_attr_setinheritsched */
    TOKEN_KW_THREAD_ATTR_GETINHERITSCHED = 367, /* thread_attr_getinheritsched */
    TOKEN_KW_THREAD_ATTR_SETSCHEDPOLICY = 368, /* thread_attr_setschedpolicy */
    TOKEN_KW_THREAD_ATTR_GETSCHEDPOLICY = 369, /* thread_attr_getschedpolicy */
    TOKEN_KW_THREAD_ATTR_SETSCHEDPARAM = 370, /* thread_attr_setschedparam */
    TOKEN_KW_THREAD_ATTR_GETSCHEDPARAM = 371, /* thread_attr_getschedparam */
    TOKEN_KW_THREAD_ATTR_SETAFFINITY_NP = 372, /* thread_attr_setaffinity_np */
    TOKEN_KW_THREAD_ATTR_GETAFFINITY_NP = 373, /* thread_attr_getaffinity_np */
    TOKEN_KW_THREAD_SETAFFINITY_NP = 374, /* thread_setaffinity_np */
    TOKEN_KW_THREAD_GETAFFINITY_NP = 375, /* thread_getaffinity_np */
    TOKEN_KW_THREAD_ATTR_SETNAME_NP = 376, /* thread_attr_setname_np */
    TOKEN_KW_THREAD_ATTR_GETNAME_NP = 377, /* thread_attr_getname_np */
    TOKEN_KW_THREAD_SETNAME_NP = 378, /* thread_setname_np */
    TOKEN_KW_THREAD_GETNAME_NP = 379, /* thread_getname_np */
    TOKEN_KW_THREAD_SETSTACKADDR_NP = 380, /* thread_setstackaddr_np */
    TOKEN_KW_THREAD_GETSTACKADDR_NP = 381, /* thread_getstackaddr_np */
    TOKEN_KW_THREAD_SETSTACKSIZE_NP = 382, /* thread_setstacksize_np */
    TOKEN_KW_THREAD_GETSTACKSIZE_NP = 383, /* thread_getstacksize_np */
    TOKEN_KW_THREAD_SETCANCELSTATE = 384, /* thread_setcancelstate */
    TOKEN_KW_THREAD_GETCANCELSTATE = 385, /* thread_getcancelstate */
    TOKEN_KW_THREAD_SETCANCELTYPE = 386, /* thread_setcanceltype */
    TOKEN_KW_THREAD_GETCANCELTYPE = 387, /* thread_getcanceltype */
    TOKEN_KW_THREAD_CANCEL = 388, /* thread_cancel */
    TOKEN_KW_THREAD_TESTCANCEL = 389, /* thread_testcancel */
    TOKEN_KW_THREAD_CLEANUP_PUSH = 390, /* thread_cleanup_push */
    TOKEN_KW_THREAD_CLEANUP_POP = 391, /* thread_cleanup_pop */
    TOKEN_KW_THREAD_SIGMASK = 392, /* thread_sigmask */
    TOKEN_KW_THREAD_KILL = 393, /* thread_kill */
    TOKEN_KW_THREAD_SIGQUEUE = 394, /* thread_sigqueue */
    TOKEN_KW_PTHREAD_ATFORK = 395, /* pthread_atfork */
    TOKEN_KW_FORK = 396, /* fork */
    TOKEN_KW_EXEC = 397, /* exec */
    TOKEN_KW_EXECL = 398, /* execl */
    TOKEN_KW_EXECV = 399, /* execv */
    TOKEN_KW_EXECLE = 400, /* execle */
    TOKEN_KW_EXECVE = 401, /* execve */
    TOKEN_KW_EXECLP = 402, /* execlp */
    TOKEN_KW_EXECVP = 403, /* execvp */
    TOKEN_KW_EXECVPE = 404, /* execvpe */
    TOKEN_KW_FEXECVE = 405, /* fexecve */
    TOKEN_KW_WAIT = 406, /* wait */
    TOKEN_KW_WAITPID = 407, /* waitpid */
    TOKEN_KW_WAITID = 408, /* waitid */
    TOKEN_KW_WAIT3 = 409, /* wait3 */
    TOKEN_KW_WAIT4 = 410, /* wait4 */
    TOKEN_KW_EXIT = 411, /* exit */
    TOKEN_KW__EXIT = 412, /* _exit */
    TOKEN_KW__EXITGROUP = 413, /* _exit_group */
    TOKEN_KW_ATEXIT = 414, /* atexit */
    TOKEN_KW_ON_EXIT = 415, /* on_exit */
    TOKEN_KW_GETPID = 416, /* getpid */
    TOKEN_KW_GETPPID = 417, /* getppid */
    TOKEN_KW_GETPGID = 418, /* getpgid */
    TOKEN_KW_SETPGID = 419, /* setpgid */
    TOKEN_KW_GETPGRP = 420, /* getpgrp */
    TOKEN_KW_SETPGRP = 421, /* setpgrp */
    TOKEN_KW_GETSID = 422, /* getsid */
    TOKEN_KW_SETSID = 423, /* setsid */
    TOKEN_KW_GETUID = 424, /* getuid */
    TOKEN_KW_SETEUID = 425, /* seteuid */
    TOKEN_KW_GETEUID = 426, /* geteuid */
    TOKEN_KW_SETUID = 427, /* setuid */
    TOKEN_KW_GETGID = 428, /* getgid */
    TOKEN_KW_SETEGID = 429, /* setegid */
    TOKEN_KW_GETEGID = 430, /* getegid */
    TOKEN_KW_SETGID = 431, /* setgid */
    TOKEN_KW_GETGROUPS = 432, /* getgroups */
    TOKEN_KW_SETGROUPS = 433, /* setgroups */
    TOKEN_KW_GETLOGIN = 434, /* getlogin */
    TOKEN_KW_SETLOGIN = 435, /* setlogin */
    TOKEN_KW_GETPWNAM = 436, /* getpwnam */
    TOKEN_KW_GETPWUID = 437, /* getpwuid */
    TOKEN_KW_GETGRNAM = 438, /* getgrnam */
    TOKEN_KW_GETGRGID = 439, /* getgrgid */
    TOKEN_KW_GETHOSTNAME = 440, /* gethostname */
    TOKEN_KW_SETHOSTNAME = 441, /* sethostname */
    TOKEN_KW_GETDOMAINNAME = 442, /* getdomainname */
    TOKEN_KW_SETDOMAINNAME = 443, /* setdomainname */
    TOKEN_KW_UNAME = 444, /* uname */
    TOKEN_KW_SYSINFO = 445, /* sysinfo */
    TOKEN_KW_GETRUSAGE = 446, /* getrusage */
    TOKEN_KW_GETRUSAGE_CHILDREN = 447, /* getrusage_children */
    TOKEN_KW_GETRUSAGE_THREAD = 448, /* getrusage_thread */
    TOKEN_KW_TIMES = 449, /* times */
    TOKEN_KW_CLOCK = 450, /* clock */
    TOKEN_KW_CLOCK_GETTIME = 451, /* clock_gettime */
    TOKEN_KW_CLOCK_SETTIME = 452, /* clock_settime */
    TOKEN_KW_CLOCK_GETRES = 453, /* clock_getres */
    TOKEN_KW_CLOCK_ADJTIME = 454, /* clock_adjtime */
    TOKEN_KW_NANOSLEEP = 455, /* nanosleep */
    TOKEN_KW_USLEEP = 456, /* usleep */
    TOKEN_KW_SLEEP = 457, /* sleep */
    TOKEN_KW_ALARM = 458, /* alarm */
    TOKEN_KW_SETITIMER = 459, /* setitimer */
    TOKEN_KW_GETITIMER = 460, /* getitimer */
    TOKEN_KW_TIMER_CREATE = 461, /* timer_create */
    TOKEN_KW_TIMER_DELETE = 462, /* timer_delete */
    TOKEN_KW_TIMER_SETTIME = 463, /* timer_settime */
    TOKEN_KW_TIMER_GETTIME = 464, /* timer_gettime */
    TOKEN_KW_TIMER_GETOVERRUN = 465, /* timer_getoverrun */
    TOKEN_KW_SIGNAL = 466, /* signal */
    TOKEN_KW_SIGACTION = 467, /* sigaction */
    TOKEN_KW_SIGPROCMASK = 468, /* sigprocmask */
    TOKEN_KW_SIGPENDING = 469, /* sigpending */
    TOKEN_KW_SIGSUSPEND = 470, /* sigsuspend */
    TOKEN_KW_SIGWAIT = 471, /* sigwait */
    TOKEN_KW_SIGWAITINFO = 472, /* sigwaitinfo */
    TOKEN_KW_SIGTIMEDWAIT = 473, /* sigtimedwait */
    TOKEN_KW_SIGQUEUE = 474, /* sigqueue */
    TOKEN_KW_SIGKILL = 475, /* sigkill */
    TOKEN_KW_SIGSTOP = 476, /* sigstop */
    TOKEN_KW_SIGCONT = 477, /* sigcont */
    TOKEN_KW_SIGINT = 478, /* sigint */
    TOKEN_KW_SIGTERM = 479, /* sigterm */
    TOKEN_KW_SIGABRT = 480, /* sigabrt */
    TOKEN_KW_SIGSEGV = 481, /* sigsegv */
    TOKEN_KW_SIGFPE = 482, /* sigfpe */
    TOKEN_KW_SIGILL = 483, /* sigill */
    TOKEN_KW_SIGBUS = 484, /* sigbus */
    TOKEN_KW_SIGPIPE = 485, /* sigpipe */
    TOKEN_KW_SIGALRM = 486, /* sigalrm */
    TOKEN_KW_SIGCHLD = 487, /* sigchld */
    TOKEN_KW_SIGHUP = 488, /* sighup */
    TOKEN_KW_SIGQUIT = 489, /* sigquit */
    TOKEN_KW_SIGTRAP = 490, /* sigtrap */
    TOKEN_KW_SIGSYS = 491, /* sigsys */
    TOKEN_KW_SIGURG = 492, /* sigurg */
    TOKEN_KW_SIGXCPU = 493, /* sigxcpu */
    TOKEN_KW_SIGXFSZ = 494, /* sigxfsz */
    TOKEN_KW_SIGVTALRM = 495, /* sigvtalrm */
    TOKEN_KW_SIGPROF = 496, /* sigprof */
    TOKEN_KW_SIGWINCH = 497, /* sigwinch */
    TOKEN_KW_SIGIO = 498, /* sigio */
    TOKEN_KW_SIGPOLL = 499, /* sigpoll */
    TOKEN_KW_SIGPWR = 500, /* sigpwr */
    TOKEN_KW_SIGUNUSED = 501, /* sigunused */
    TOKEN_KW_SIGRTMIN = 502, /* sigrtmin */
    TOKEN_KW_SIGRTMAX = 503, /* sigrtmax */
    TOKEN_KW_SIGEMPTYSET = 504, /* sigemptyset */
    TOKEN_KW_SIGFILLSET = 505, /* sigfillset */
    TOKEN_KW_SIGADDSET = 506, /* sigaddset */
    TOKEN_KW_SIGDELSET = 507, /* sigdelset */
    TOKEN_KW_SIGISMEMBER = 508, /* sigismember */
    TOKEN_KW_SIGSETOPS = 509, /* sigsetops */
    TOKEN_KW_PAUSE = 510, /* pause */
    TOKEN_KW_KILL = 511, /* kill */
    TOKEN_KW_KILLPG = 512, /* killpg */
    TOKEN_KW_RAISE = 513, /* raise */
    TOKEN_KW_SIGSETJMP = 514, /* sigsetjmp */
    TOKEN_KW_SIGLONGJMP = 515, /* siglongjmp */
    TOKEN_KW_SETJMP = 516, /* setjmp */
    TOKEN_KW_LONGJMP = 517, /* longjmp */
    TOKEN_KW___BUILTIN_SETJMP = 518, /* __builtin_setjmp */
    TOKEN_KW___BUILTIN_LONGJMP = 519, /* __builtin_longjmp */
    TOKEN_KW___BUILTIN_RETURN_ADDRESS = 520, /* __builtin_return_address */
    TOKEN_KW___BUILTIN_FRAME_ADDRESS = 521, /* __builtin_frame_address */
    TOKEN_KW___BUILTIN_EXPECT = 522, /* __builtin_expect */
    TOKEN_KW___BUILTIN_EXPECT_WITH_PROBABILITY = 523, /* __builtin_expect_with_probability */
    TOKEN_KW___BUILTIN_UNREACHABLE = 524, /* __builtin_unreachable */
    TOKEN_KW___BUILTIN_TRAP = 525, /* __builtin_trap */
    TOKEN_KW___BUILTIN_ABORT = 526, /* __builtin_abort */
    TOKEN_KW___BUILTIN_ASSUME = 527, /* __builtin_assume */
    TOKEN_KW___BUILTIN_ASSUME_ALIGNED = 528, /* __builtin_assume_aligned */
    TOKEN_KW___BUILTIN_PREFETCH = 529, /* __builtin_prefetch */
    TOKEN_KW___BUILTIN_CLZ = 530, /* __builtin_clz */
    TOKEN_KW___BUILTIN_CTZ = 531, /* __builtin_ctz */
    TOKEN_KW___BUILTIN_POPCOUNT = 532, /* __builtin_popcount */
    TOKEN_KW___BUILTIN_PARITY = 533, /* __builtin_parity */
    TOKEN_KW___BUILTIN_FFS = 534, /* __builtin_ffs */
    TOKEN_KW___BUILTIN_BSWAP = 535, /* __builtin_bswap */
    TOKEN_KW___BUILTIN_BSWAP16 = 536, /* __builtin_bswap16 */
    TOKEN_KW___BUILTIN_BSWAP32 = 537, /* __builtin_bswap32 */
    TOKEN_KW___BUILTIN_BSWAP64 = 538, /* __builtin_bswap64 */
    TOKEN_KW___BUILTIN_BYTEORDER = 539, /* __builtin_byteorder */
    TOKEN_KW___BUILTIN_ENDIAN = 540, /* __builtin_endian */
    TOKEN_KW___BUILTIN_NTOHS = 541, /* __builtin_ntohs */
    TOKEN_KW___BUILTIN_HTONS = 542, /* __builtin_htons */
    TOKEN_KW___BUILTIN_NTOHL = 543, /* __builtin_ntohl */
    TOKEN_KW___BUILTIN_HTONL = 544, /* __builtin_htonl */
    TOKEN_KW___BUILTIN_CONSTANT_P = 545, /* __builtin_constant_p */
    TOKEN_KW___BUILTIN_CHOOSE_EXPR = 546, /* __builtin_choose_expr */
    TOKEN_KW___BUILTIN_TYPES_COMPATIBLE_P = 547, /* __builtin_types_compatible_p */
    TOKEN_KW___BUILTIN_IS_CONSTANT = 548, /* __builtin_is_constant */
    TOKEN_KW___BUILTIN_HAS_ATTRIBUTE = 549, /* __builtin_has_attribute */
    TOKEN_KW___BUILTIN_HAS_FEATURE = 550, /* __builtin_has_feature */
    TOKEN_KW___BUILTIN_HAS_INCLUDE = 551, /* __builtin_has_include */
    TOKEN_KW___BUILTIN_HAS_EXTENSION = 552, /* __builtin_has_extension */
    TOKEN_KW___BUILTIN_HAS_WARNING = 553, /* __builtin_has_warning */
    TOKEN_KW___BUILTIN_HAS_DECLSPEC = 554, /* __builtin_has_declspec */
    TOKEN_KW___BUILTIN_HAS_CPP_ATTRIBUTE = 555, /* __builtin_has_cpp_attribute */
    TOKEN_KW___BUILTIN_LINE = 556, /* __builtin_LINE */
    TOKEN_KW___BUILTIN_FILE = 557, /* __builtin_FILE */
    TOKEN_KW___BUILTIN_FUNCTION = 558, /* __builtin_FUNCTION */
    TOKEN_KW___BUILTIN_FUNC = 559, /* __builtin_FUNC */
    TOKEN_KW___BUILTIN_PRETTY_FUNCTION = 560, /* __builtin_PRETTY_FUNCTION */
    TOKEN_KW___BUILTIN_COLUMN = 561, /* __builtin_COLUMN */
    TOKEN_KW___BUILTIN_COMPILER = 562, /* __builtin_compiler */
    TOKEN_KW___BUILTIN_VERSION = 563, /* __builtin_version */
    TOKEN_KW___BUILTIN_TIMESTAMP = 564, /* __builtin_timestamp */
    TOKEN_KW___BUILTIN_DATE = 565, /* __builtin_date */
    TOKEN_KW___BUILTIN_TIME = 566, /* __builtin_time */
    TOKEN_KW___BUILTIN_STDC_HOSTED = 567, /* __builtin_STDC_HOSTED */
    TOKEN_KW___BUILTIN_STDC_VERSION = 568, /* __builtin_STDC_VERSION */
    TOKEN_KW___BUILTIN_STDC_UTF_16 = 569, /* __builtin_STDC_UTF_16 */
    TOKEN_KW___BUILTIN_STDC_UTF_32 = 570, /* __builtin_STDC_UTF_32 */
    TOKEN_KW___BUILTIN_STDC_NO_ATOMICS = 571, /* __builtin_STDC_NO_ATOMICS */
    TOKEN_KW___BUILTIN_STDC_NO_COMPLEX = 572, /* __builtin_STDC_NO_COMPLEX */
    TOKEN_KW___BUILTIN_STDC_NO_THREADS = 573, /* __builtin_STDC_NO_THREADS */
    TOKEN_KW___BUILTIN_STDC_NO_VLA = 574, /* __builtin_STDC_NO_VLA */
    TOKEN_KW___BUILTIN_STDC_IEC_559 = 575, /* __builtin_STDC_IEC_559 */
    TOKEN_KW___BUILTIN_STDC_IEC_559_COMPLEX = 576, /* __builtin_STDC_IEC_559_COMPLEX */
    TOKEN_KW___BUILTIN_STDC_ISO_10646 = 577, /* __builtin_STDC_ISO_10646 */
    TOKEN_KW___BUILTIN_STDC_LIB_EXT1 = 578, /* __builtin_STDC_LIB_EXT1 */
    TOKEN_KW___BUILTIN_STDC_ANALYZABLE = 579, /* __builtin_STDC_ANALYZABLE */
    TOKEN_KW___BUILTIN_STDC_WANT_LIB_EXT1 = 580, /* __builtin_STDC_WANT_LIB_EXT1 */
    TOKEN_KW___BUILTIN_STDC_MATH_H = 581, /* __builtin_STDC_MATH_H */
    TOKEN_KW___BUILTIN_STDC_MATH_ERRNO = 582, /* __builtin_STDC_MATH_ERRNO */
    TOKEN_KW___BUILTIN_STDC_MATH_ERREXCEPT = 583, /* __builtin_STDC_MATH_ERREXCEPT */
    TOKEN_KW___BUILTIN_STDC_MATH_FENV_ACCESS = 584, /* __builtin_STDC_MATH_FENV_ACCESS */
    TOKEN_KW___BUILTIN_STDC_MATH_FAST_MATH = 585, /* __builtin_STDC_MATH_FAST_MATH */
    TOKEN_KW___BUILTIN_STDC_MATH_FINITE_MATH_ONLY = 586, /* __builtin_STDC_MATH_FINITE_MATH_ONLY */
    TOKEN_KW___BUILTIN_STDC_MATH_CONTRACT = 587, /* __builtin_STDC_MATH_CONTRACT */
    TOKEN_KW___BUILTIN_STDC_MATH_EVAL_METHOD = 588, /* __builtin_STDC_MATH_EVAL_METHOD */
    TOKEN_KW___BUILTIN_STDC_MATH_FENV_ROUND = 589, /* __builtin_STDC_MATH_FENV_ROUND */
    TOKEN_KW___BUILTIN_STDC_MATH_FENV_TRAPS = 590, /* __builtin_STDC_MATH_FENV_TRAPS */
    TOKEN_KW___BUILTIN_STDC_MATH_FENV_DETERM = 591, /* __builtin_STDC_MATH_FENV_DETERM */
    TOKEN_KW___BUILTIN_STDC_MATH_FENV_CX_LIMITED_RANGE = 592, /* __builtin_STDC_MATH_FENV_CX_LIMITED_RANGE */
    TOKEN_KW___BUILTIN_STDC_MATH_FENV_CX_FINITE_MATH_ONLY = 593, /* __builtin_STDC_MATH_FENV_CX_FINITE_MATH_ONLY */
    TOKEN_KW___BUILTIN_STDC_MATH_FENV_CX_CONTRACT = 594, /* __builtin_STDC_MATH_FENV_CX_CONTRACT */
    TOKEN_KW___BUILTIN_STDC_MATH_FENV_CX_EVAL_METHOD = 595, /* __builtin_STDC_MATH_FENV_CX_EVAL_METHOD */
    TOKEN_KW___BUILTIN_STDC_MATH_FENV_CX_FENV_ROUND = 596, /* __builtin_STDC_MATH_FENV_CX_FENV_ROUND */
    TOKEN_KW___BUILTIN_STDC_MATH_FENV_CX_FENV_TRAPS = 597, /* __builtin_STDC_MATH_FENV_CX_FENV_TRAPS */
    TOKEN_KW___BUILTIN_STDC_MATH_FENV_CX_FENV_DETERM = 598, /* __builtin_STDC_MATH_FENV_CX_FENV_DETERM */
    TOKEN_KW___BUILTIN_STDC_MATH_FENV_CX_CX_LIMITED_RANGE = 599, /* __builtin_STDC_MATH_FENV_CX_CX_LIMITED_RANGE */
    TOKEN_KW___BUILTIN_STDC_MATH_FENV_CX_CX_FINITE_MATH_ONLY = 600, /* __builtin_STDC_MATH_FENV_CX_CX_FINITE_MATH_ONLY */
    TOKEN_COUNT
} TokenType;

/* Token 结构体 */
typedef struct {
    TokenType type;
    char* value;
    int line;
    int col;
    int pos;
    int length;
} Token;

/* Token 列表 */
typedef struct {
    Token* tokens;
    int count;
    int capacity;
} TokenList;

/* 词法分析器状态 */
typedef struct {
    const char* source;
    int length;
    int pos;
    int line;
    int col;
    TokenList tokens;
    int error_count;
    char** errors;
} Lexer;

/* 函数声明 */
Lexer* lexer_create(const char* source);
void lexer_destroy(Lexer* lexer);
TokenList lexer_tokenize(Lexer* lexer);
Token lexer_next_token(Lexer* lexer);
Token lexer_peek_token(Lexer* lexer);
int lexer_has_error(Lexer* lexer);
const char* token_type_name(TokenType type);
const char* token_type_description(TokenType type);

#endif /* AURORA_LEXER_H */