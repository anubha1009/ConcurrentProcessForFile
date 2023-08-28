import concurrent.futures

def process_file_part(file_part, keyword):
    found = False
    with open(file_part, 'r') as file:
        for line in file:
            if keyword in line:
                found = True
                break
    return found

def split_and_search_file(file_path, keyword):
    file_parts = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        words_array = lines[0].split(' ')
        words_per_file = len(words_array) // 4
        for i in range(4):
            file_part = 'file_part_{}.txt'.format(i) #file names
            file_parts.append(file_part)
            with open(file_part, 'w') as f:
                f.write(' '.join(words_array[i * words_per_file: (i + 1) * words_per_file])) #write words in those files
                f.close()
        

    found = False
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for file_part in file_parts:
            futures.append(executor.submit(process_file_part, file_part, keyword))
        for future in futures:
            if future.result():
                found = True
                break
    return found

def main():
    file = input("Enter the file to upload:")
    keyword = input("Enter the keyword to search:")

    if file and keyword:
        file_path = file

        found = split_and_search_file(file_path, keyword)

        if found:
            print("Keyword found in the file.")
           
        else:
            print("Keyword not found in the file.")
            
    else:
        print("Please upload a file")

if __name__ == "__main__":
    main()