#! /usr/bin/python
# Written By Tom Paulus, @tompaulus, www.tompaulus.com

from lib.tidylib import tidy_document

from modules.properties import Property


class GenEmail(object):
    temp_summary = """<tr>
                <td valign="top" class="preheaderContent"
                style="padding-top:10px; padding-right:20px; padding-bottom:10px; padding-left:20px;"
                mc:edit="preheader_content00">
                {text}
                </td>
                </tr>"""

    temp_header_image = """<tr>
                    <td valign="top" class="headerContent">
                    <img src="{url}" style="max-width:600px;" id="headerImage" mc:label="header_image"
                    mc:edit="header_image" mc:allowdesigner mc:allowtext/>
                    </td>
                    </tr>"""

    temp_body_r1 = """<tr>
                 <td valign="top" class="bodyContent" mc:edit="body_content00">
                 <h1>
                      {title}
                 </h1>
                 <h3>
                     {subtitle}
                 </h3>
                     {text}
                 </td>
                 </tr>"""

    temp_body_image = """<tr>
                    <td class="bodyContent" style="padding-top:0; padding-bottom:0;">
                    <img src="{url}" style="max-width:560px;" id="bodyImage" mc:label="body_image"
                    mc:edit="body_image" mc:allowtext/>
                    </td>
                    </tr>"""

    temp_body_r2 = """<tr>
                 <td valign="top" class="bodyContent" mc:edit="body_content01">
                 <h2>{title}</h2>
                 <h4>{subtitle}</h4>
                 {text}
                 </td>
                  </tr>"""

    temp_column_row = """<tr mc:repeatable>
                    <td align="left" valign="top" style="padding-bottom:0;">
                    {left_column}
                    {right_column}
                    </td>
                    </tr>"""

    temp_left_column = """<table align="left" border="0" cellpadding="0" cellspacing="0"class="templateColumnContainer">
                     <tr>
                        <td class="leftColumnContent">
                            <img src="{url}" style="max-width:260px;" class="columnImage" mc:label="left_column_image"
                            mc:edit="left_column_image"/>
                        </td>
                     </tr>
                     <tr>
                        <td valign="top" class="leftColumnContent" mc:edit="left_column_content">
                        <h3>
                            {title}
                        </h3>
                            {text}
                        </td>
                     </tr>
                     </table>"""

    temp_right_column = """<table align="right" border="0" cellpadding="0" cellspacing="0"
                            class="templateColumnContainer">
                      <tr>
                        <td class="rightColumnContent">
                            <img src="{url}" style="max-width:260px;" class="columnImage"  mc:label="right_column_image"
                            mc:edit="right_column_image"/>
                        </td>
                      </tr>
                        <tr>
                        <td valign="top" class="rightColumnContent" mc:edit="right_column_content">
                            <h3>
                                {title}
                            </h3>
                            {text}
                        </td>
                      </tr>
                      </table>"""

    temp_footer = """<td align="center" valign="top">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" id="templateFooter">
                <tr>
                   <td valign="top" class="footerContent" mc:edit="footer_content00">
                        {social}
                   </td>
                </tr>
                <tr>
                    <td valign="top" class="footerContent" style="padding-top:0;" mc:edit="footer_content01">
                        {copyright}
                    </td>
                </tr>
                <tr>
                    <td valign="top" class="footerContent" style="padding-top:0;" mc:edit="footer_content02">
                        {unsubscribe}
                    </td>
                </tr>
                </table>
                </td>"""

    @staticmethod
    def replace(string, replacement_dict):
        for replacement_num in range(0, len(replacement_dict.keys())):
            replacement_tag = '{%s}' % str(list(replacement_dict.keys())[replacement_num])
            replacement_value = replacement_dict[list(replacement_dict.keys())[replacement_num]]
            string = string.replace(replacement_tag, replacement_value)

        return string

    def __init__(self):
        self.title = 'Good Morning'
        self.summary = {'text': ''}
        self.header_image = {'url': ''}
        self.body_r1 = {'title': '', 'subtitle': '', 'text': ''}
        self.body_image = {'url': ''}
        self.body_r2 = {'title': '', 'subtitle': '', 'text': ''}
        self.columns = []
        self.footer = {'social': '', 'copyright': '', 'unsubscribe': ''}
        self.modules = {'summary': '', 'header_image': '',
                        'body_r1': '', 'body_image': '',
                        'body_r2': '', 'columns': '',
                        'footer': ''}

    def generate(self):
        self.modules['title'] = self.title

        if self.summary.values() != ['']:
            s = self.replace(GenEmail.temp_summary, self.summary)
            self.modules['summary'] = s

        if self.header_image.values() != ['']:
            s = self.replace(GenEmail.temp_header_image, self.header_image)
            self.modules['header_image'] = s

        if self.body_r1.values() != ['']:
            s = self.replace(GenEmail.temp_body_r1, self.body_r1)
            self.modules['body_r1'] = s

        if self.body_image.values() != ['']:
            s = self.replace(GenEmail.temp_body_image, self.body_image)
            self.modules['body_image'] = s

        if self.body_r2.values() != ['']:
            s = self.replace(GenEmail.temp_body_r2, self.body_r2)
            self.modules['body_r2'] = s

        column_html = ''
        for column_num in range(0, len(self.columns), 2):
            row = {'left_column': '', 'right_column': ''}
            for c in range(column_num, (column_num + 2)):
                if c % 2 == 0:
                    # Left Side
                    row['left_column'] = self.replace(GenEmail.temp_left_column, self.columns[c])
                elif c % 2 == 1:
                    #Right Side
                    row['right_column'] = self.replace(GenEmail.temp_right_column, self.columns[c])
            column_html += self.replace(GenEmail.temp_column_row, row)

        self.modules['columns'] = column_html

        with open(Property.email_save_loc, 'w') as final_email:
            with open(Property.email_template_loc, 'r') as email_template:
                message = email_template.read()
            message = self.replace(message, self.modules)
            tidy, errors = tidy_document(message)
            final_email.write(tidy)
