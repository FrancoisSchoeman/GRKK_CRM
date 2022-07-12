
def check_file(file):
    if file.name.endswith('.csv') or file.name.endswith('.xlsx'):
        return True
    else:
        return False