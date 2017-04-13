import re
# for counting words in a file
data = [line.strip() for line in open("testfile1.txt", 'r')] # strips the file where there are white spaces and reads it
num_words = 0
pcount = 0
for item in data:
    num_words += len(item.split())                                  # counts number of words in the file

print "Word Count:",num_words                                      #number of words including punctuation marks

# for counting sentences in a file
with open('testfile1.txt','r') as content_file:
    content = content_file.read()
    modified = re.sub('Dr.','Doctor',content)                      #Substituting Dr. as Doctor in the file
    modified1 = re.sub('Mr.','Mister',modified)                     #Substituting Mr. as Mister in the file
    modified2 = re.sub('Ms.','Miss',modified1)                      #Substituting Ms. as Miss in the file
    lineCount = re.findall('\. [A-Z]|\.\"|\.\)|\.\n',modified2)     #Split the file whenever it sees full stop followed by whitespace and Capital alphabet.
print "Line Count:",len(lineCount)

# for counting paragraphs in a file
paragraph = 0
prev = '\n'

with open ('testfile1.txt') as fname:
    for line in fname:
        if line != '\n' and prev == '\n' or prev == ' \n':          #counting number of paragrahs by comparing \n with prev \n
            paragraph += 1
        prev = line
print "Paragraph Count:",paragraph


