from passlib.hash import sha256_crypt




print(sha256_crypt.verify("1234567", "$5$rounds=535000$aU9bbyl8yhx9.ezs$54SMhyFn/1RHhhpz35ZIiuPpIYON/NH4/cErJwR9WS8"))