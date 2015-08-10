__author__ = 'Syngularity'

import json
import httplib
import urllib


class JsCompressor:
    def __init__(self, js_code, js_version='ECMASCRIPT5', compilation_level='ADVANCED_OPTIMIZATIONS'):
        self.js_code = js_code
        self.js_version = js_version
        self.compilation_level = compilation_level

    def js_compress(self):
        params = ([
                ('js_code', self.js_code),
                ('compilation_level', self.compilation_level),
                ('output_format', 'json'),
                ('output_info', 'compiled_code'),
                ('output_info', 'errors'),
                ('output_info', 'warnings'),
                ('output_info', 'statistics'),
                ('language', self.js_version)
                ])

        request_parameters = urllib.urlencode(params)
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        connection = httplib.HTTPConnection('closure-compiler.appspot.com')
        connection.request('POST', '/compile', request_parameters, headers)
        response = connection.getresponse()
        closure_json_response = json.loads(response.read())
        connection.close()

        if 'errors' in closure_json_response:
            closure_error_handling(closure_json_response['errors'])
            exit()

        if 'serverErrors' in closure_json_response:
            server_error_handling(closure_json_response['serverErrors'])
            exit()

        if 'compiledCode' in closure_json_response:
            print_statistic(closure_json_response['statistics'])
            if 'warnings' in closure_json_response:
                closure_warning_handling(closure_json_response['warnings'])
            return closure_json_response['compiledCode']


def closure_error_handling(closure_errors):
    print len(closure_errors), 'error/errors was/were found in your code! \n'
    for error in closure_errors:
        print 'Error in line:', error['lineno'], 'at character:', error['charno']
        print 'Error type:', error['type']
        print error['line']
        print ' ' * int(error['charno']), '^'
        print error['error']
        print '_' * 10


def closure_warning_handling(closure_warnings):
    print len(closure_warnings), 'warning/warnings was/were found in your code! \n'
    for warning in closure_warnings:
        print 'Warning in line:', warning['lineno'], 'at character:', warning['charno']
        print 'Warning type:', warning['type']
        print warning['line']
        print ' ' * int(warning['charno']), '^'
        print warning['warning']
        print '_' * 10


def server_error_handling(closure_server_error):
    print 'Server error/errors!'
    for server_e in closure_server_error:
        print 'Error code:', server_e['code']
        print 'Error message:', server_e['error']
        print '_' * 10

def print_statistic(closure_statistics):
    print '_' * 20
    print 'Compilation was a success!\nClosure compiler statistics:'
    print 'Original size:', closure_statistics['originalSize'], 'bytes'
    print 'Compressed size:', closure_statistics['compressedSize'], 'bytes'
    print 'You saved', closure_statistics['originalSize'] - closure_statistics['compressedSize'], 'bytes off'
    print 'Compiling your code takes', closure_statistics['compileTime']
    print '_' * 20

def main():
    js_f = open('html\\game\\js\\game.js').read()
    js_c = JsCompressor(js_f, js_version='ECMASCRIPT5')
    print js_c.js_compress()


if __name__ == "__main__":
    main()
