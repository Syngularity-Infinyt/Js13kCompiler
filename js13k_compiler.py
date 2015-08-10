__author__ = 'Syngularity'

# from BeautifulSoup import BeautifulSoup
from htmlmin import minify
from bs4 import BeautifulSoup
import re
import os
import sys

import js_compress
import css_compressor


class IndexHtmlExtractor:
    def __init__(self, path_to_index_html):
        self.index_html_soup = BeautifulSoup(read_file(path_to_index_html), 'lxml')

    def get_inline_js_list(self):
        return self.index_html_soup('script', type='text/javascript')

    def get_js_file_list(self):
            return self.index_html_soup('script', src=re.compile('\.+'))

    def get_inline_css_list(self):
        return self.index_html_soup('style')

    def get_css_file_list(self):
        return self.index_html_soup('link', rel="stylesheet")


class JsParser:
    def __init__(self, js_file_path, js_v='ECMASCRIPT5', co_lvl='ADVANCED_OPTIMIZATIONS'):
        self.js_code = read_file(js_file_path)
        self.js_code_min = js_compress.JsCompressor(self.js_code, js_version=js_v, compilation_level=co_lvl)

    def get_js_min(self):
        return self.js_code_min.js_compress()


class CssParser:
    def __init__(self, css_file_path):
        self.css_code = read_file(css_file_path)
        self.css_code_min = css_compressor.CssCompressor(self.css_code)

    def get_css_min(self):
        return self.css_code_min.css_compress()


class HtmlParser:
    def __init__(self, html_file_path):
        self.html_code = read_file(html_file_path).decode('unicode-escape')
        self.html_code_min = minify(self.html_code, remove_comments=True, remove_empty_space=True)


class ProjectCompressor:
    def __init__(self, path_to_index_html):
        self.extracted_index_html = IndexHtmlExtractor(path_to_index_html)
        ch_cwd_to_index_root(path_to_index_html)

    def compress_project(self):

        for i in self.extracted_index_html.index_html_soup('script', type='text/javascript'):
            i.string = js_compress.JsCompressor(i.string).js_compress()

        for i in self.extracted_index_html.index_html_soup('style'):
            i.string = css_compressor.CssCompressor(i.string).css_compress()

        ls_j = self.extracted_index_html.get_js_file_list()
        for i in ls_j:
            temp_tag = self.extracted_index_html.index_html_soup.new_tag('script')
            temp_tag['type'] = 'text/javascript'
            temp_tag.string = JsParser(i['src']).get_js_min()
            self.extracted_index_html.get_js_file_list()[0].replace_with(temp_tag)

        ls_c = self.extracted_index_html.get_css_file_list()
        for i in ls_c:
            temp_tag = self.extracted_index_html.index_html_soup.new_tag('style')
            temp_tag.string = CssParser(i['href']).get_css_min()
            self.extracted_index_html.get_css_file_list()[0].replace_with(temp_tag)

        html_code_wc = str(self.extracted_index_html.index_html_soup.prettify())
        print html_code_wc
        return minify(html_code_wc.decode('unicode-escape'), remove_comments=True, remove_empty_space=True)


def file_concat(list_of_files):
    final_file = str()
    for file_ in list_of_files:
        with open(file_) as f:
            final_file += ('\n' + f.read())
    return final_file


def ch_cwd_to_index_root(index_file_path):
    os.chdir(os.path.abspath(os.path.dirname(index_file_path)))


def read_file(file_path):
    try:
        return open(file_path, 'r').read()
    except IOError as e:
        print 'I/O error(', e.errno, '):', e.strerror
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise


def main():
    h = ProjectCompressor('html\index.html')
    h.compress_project()

if __name__ == '__main__':
    main()
