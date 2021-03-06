import aiofiles


async def append_to_file(data,
                         file,):
    encoding = "utf-16"
    data_flat = f"{data}\n"
    async with aiofiles.open(file,
                             "a+",
                             encoding=encoding) as outfile:
        await outfile.write(data_flat)
    return True


def append_to_file_blocking(data,
                            file,):
    encoding = "utf-16"
    data_flat = f"{data}\n"
    with open(file,
              "a+",
              encoding=encoding) as outfile:
        outfile.write(data_flat)
    return True
