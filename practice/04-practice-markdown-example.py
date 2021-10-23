from mdutils.mdutils import MdUtils


mdFile = MdUtils(file_name='Example_Markdown',title='Markdown File Example....')

mdFile.new_header(level=1, title='Atx Header 1')
mdFile.new_header(level=2, title='Atx Header 2')
mdFile.new_header(level=3, title='Atx Header 3')
mdFile.new_header(level=4, title='Atx Header 4')
mdFile.new_header(level=5, title='Atx Header 5')
mdFile.new_header(level=6, title='Atx Header 6')

mdFile.new_header(level=1, title='Setext Header 1', style='setext')
mdFile.new_header(level=2, title='Setext Header 2', style='setext')

mdFile.new_table_of_contents(table_title='Contents', depth=2)

mdFile.new_paragraph("Using ``new_paragraph`` method you can very easily add a new paragraph" 
					 " This example of paragraph has been added using this method. Moreover,"
					 "``new_paragraph`` method make your live easy because it can give format" 
					 " to the text. Lets see an example:")

mdFile.new_paragraph("This is an example of text in which has been added color, bold and italics text.", bold_italics_code='bi', color='purple')


mdFile.new_line("This is an example of line break which has been created with ``new_line`` method.")


mdFile.write("The following text has been written with ``write`` method. You can use markdown directives to write:"
			 "**bold**, _italics_, ``inline_code``... or ")
mdFile.write("use the following available parameters:  \n")

mdFile.write('  \n')
mdFile.write('bold_italics_code', bold_italics_code='bic')
mdFile.write('  \n')
mdFile.write('Text color', color='green')
mdFile.write('  \n')
mdFile.write('Align Text to center', align='center')


list_of_strings = ["Items", "Descriptions", "Data"]
for x in range(5):
	list_of_strings.extend(["Item " + str(x), "Description Item " + str(x), str(x)])
mdFile.new_line()
mdFile.new_table(columns=3, rows=6, text=list_of_strings, text_align='center')


mdFile.create_md_file()