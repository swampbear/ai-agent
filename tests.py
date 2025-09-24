from functions.get_files_info import get_files_info

err = get_files_info("calculator", ".")

if err != None:
    print(err)

err = get_files_info("calculator", "pkg")
if err != None:
    print(err)

err = get_files_info("calculator", "/bin")

if err != None:
    print(err)

err_slash = get_files_info("calculator","../")

if err_slash != None:
    print(err_slash)
