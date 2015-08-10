__author__ = 'Syngularity'

import re


class CssCompressor:
    def __init__(self, css_code):
        self.css_code = css_code

    def css_compress(self):
        css_code_min = re.sub(r'\s*/\*\s*\*/', "$$HACK1$$", self.css_code)  # preserve IE<6 comment hack
        css_code_min = re.sub(r'/\*[\s\S]*?\*/', "", css_code_min)
        css_code_min = css_code_min.replace("$$HACK1$$", '/**/')
        css_code_min = re.sub(r'url\((["\'])([^)]*)\1\)', r'url(\2)', css_code_min)
        css_code_min = re.sub(r'\s+', ' ', css_code_min)
        css_code_min = re.sub(r'#([0-9a-f])\1([0-9a-f])\2([0-9a-f])\3(\s|;)', r'#\1\2\3\4', css_code_min)
        css_code_min = re.sub(r':\s*0(\.\d+([cm]m|e[mx]|in|p[ctx]))\s*;', r':\1;', css_code_min)
        css_code_min = css_code_min.replace(' ', '')
        return css_code_min


def main():
    css_f = open('html\\game\\css\\game.css').read()
    css_c = CssCompressor(css_f)
    print css_c.css_compress()

if __name__ == '__main__':
    main()
