# Short ID

A short id generator.


# Usage

1. Convert between normal id and short id

    ```python
    from short_id import encode, decode

    sid = encode(123456789)  # 1ly7vk

    nid = decode(sid)  # 123456789
    ```

2. Custom your ShortID

    ```python
    from short_id import ShortID

    id_gen = ShortID('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz=-')

    # iterable
    for i, sid in enumerate(id_gen):
        print(sid)
        if i >= 10:
            break

    # next()
    for i in range(10):
        print(next(id_gen))

    # check
    print(id_gen.is_valid('d9j3=jsjf'))

    # encode and decode
    sid = id_gen.encode(123456789)
    print(sid)

    nid = id_gen.decode(sid)
    print(nid)
    ```
