# -*- coding: utf-8 -*-
"""
Created on Wed May 10 13:48:47 2017

@author: adam

The NPPES has an API to ping the database based on the URL
https://npiregistry.cms.hhs.gov/api/. and an accompanying query string
This app provides a UI to search by select criteria, and format the
returned json into readable format
"""

import datetime
import json
import logging
import requests
import tkinter

# logging config
logging.basicConfig(filename='npi_api.log', level=logging.INFO)

class NPI_API():
    def __init__(self, master):
        self.master = master
        # build windows
        # main window houses whole app
        self.mainframe = tkinter.Frame(self.master, bg='white')
        self.mainframe.pack(fill=tkinter.BOTH, expand=True)
        # entry window houses entry elements and labels
        self.entryframe = tkinter.Frame(self.mainframe, bg='white')
        self.entryframe.grid(row=0, sticky='ew')
        # button windows holds submit button
        self.buttonframe = tkinter.Frame(self.mainframe, bg='white')
        self.buttonframe.grid(row=1)
        # results window holds result provided by API
        self.resultsframe = tkinter.Frame(self.mainframe, bg='white')
        self.resultsframe.grid(row=2)
        # variables
        self.TEST_TEXT = 'this is a test, for text'
        self.wildcard_check_status = tkinter.IntVar()
        # build funcions
        self.build_grids()
        self.build_banner()
        self.build_entry_fields()
        self.build_buttons()
        self.build_results()

    def build_grids(self):
        self.mainframe.columnconfigure(0)
        self.mainframe.rowconfigure(0)
        self.mainframe.rowconfigure(1)
        self.mainframe.rowconfigure(2)
        self.entryframe.columnconfigure(0, weight=1)
        self.entryframe.columnconfigure(1, weight=1)
        self.entryframe.columnconfigure(2, weight=0)
        self.entryframe.columnconfigure(3, weight=1)
        self.entryframe.rowconfigure(0, weight=0)
        self.entryframe.rowconfigure(1, weight=0)
        self.entryframe.rowconfigure(2, weight=0)
        self.entryframe.rowconfigure(3, weight=0)
        self.buttonframe.columnconfigure(0, weight=0)
        self.buttonframe.columnconfigure(1, weight=1)
        self.buttonframe.columnconfigure(2, weight=0)
        self.buttonframe.rowconfigure(0)
        self.resultsframe.columnconfigure(0, weight=1)
        self.resultsframe.rowconfigure(0)
        self.resultsframe.rowconfigure(1, weight=1)
        self.resultsframe.rowconfigure(2, weight=1)
        self.resultsframe.rowconfigure(3, weight=1)
        self.resultsframe.rowconfigure(4, weight=1)
        self.resultsframe.rowconfigure(5, weight=1)

    def build_banner(self):
        banner = tkinter.Label(
                self.entryframe,
                text='To search for NPI, add any or all of the below fields and click search',
                fg='white',
                bg='blue',
                )
        banner.grid(
                row=0, columnspan=4,
                sticky='ew')

    def build_entry_fields(self):
        self.f_name_entry = tkinter.Entry(
                self.entryframe,
                bg='white',
                takefocus=True
                )
        self.f_name_lbl = tkinter.Label(
                self.entryframe,
                text='First Name:',
                bg='white'
                )
        self.f_name_entry.grid(
                row=1, column=1,
                sticky='ew',
                pady=5,
                padx=5,
                )
        self.f_name_lbl.grid(
                row=1, column=0,
                sticky='w',
                pady=5,
                padx=5,
                )
        self.l_name_entry = tkinter.Entry(
                self.entryframe,
                bg='white',
                )
        self.l_name_lbl = tkinter.Label(
                self.entryframe,
                text='Last Name:',
                bg='white'
                )
        self.l_name_entry.grid(
                row=1, column=3,
                sticky='ew',
                pady=5,
                padx=5,
                )
        self.l_name_lbl.grid(
                row=1, column=2,
                sticky='w',
                pady=5,
                padx=5,
                )
        self.npi_entry = tkinter.Entry(
                self.entryframe,
                bg='white',
                )
        self.npi_lbl = tkinter.Label(
                self.entryframe,
                text='NPI:',
                bg='white'
                )
        self.npi_entry.grid(
                row=2, column=1,
                sticky='ew',
                padx=5,
                pady=5,
                )
        self.npi_lbl.grid(
                row=2, column=0,
                sticky='w',
                padx=5,
                pady=5,
                )
        self.state_name_entry = tkinter.Entry(
                self.entryframe,
                bg='white',
                )
        self.state_name_lbl = tkinter.Label(
                self.entryframe,
                text='State:',
                bg='white'
                )
        self.state_name_entry.grid(
                row=2, column=3,
                sticky='ew',
                padx=5,
                pady=5,
                )
        self.state_name_lbl.grid(
                row=2, column=2,
                sticky='w',
                padx=5,
                pady=5,
                )
        self.limit_lbl = tkinter.Label(
                self.entryframe,
                text='# of results:',
                bg='white'
                )
        self.limit_entry = tkinter.Entry(
                self.entryframe,
                bg='white',
                )
        self.limit_lbl.grid(
                row=3, column=0,
                sticky='w',
                padx=5,
                pady=5,
                )
        self.limit_entry.grid(
                row=3, column=1,
                sticky='ew',
                padx=5,
                pady=5,
                )
        self.wildcard_check = tkinter.Checkbutton(
                self.entryframe,
                text='Use wildcards?',
                bg='white',
                variable=self.wildcard_check_status
                )
        self.wildcard_check.grid(
                row=3, column=3,
                sticky='ew',
                )

    def build_buttons(self):
        self.submit_btn = tkinter.Button(
                self.buttonframe,
                text='Submit',
                command=self.query_npi_api
                )
        self.submit_btn.grid(
                row=0, column=0,
                sticky='ew',
                pady=20,
                padx=20,
                )
        self.clear_btn = tkinter.Button(
                self.buttonframe,
                text='Clear',
                command=self.clear
                )
        self.clear_btn.grid(
                row=0, column=1,
                sticky='ew',
                pady=20,
                padx=20,
                )

    def build_results(self):
        self.results_win_match_records = tkinter.Label(
                self.resultsframe,
                bg='white',
                )
        self.results_win_match_records.grid(
                row=0,
                sticky='news')
        self.results_win_data_1 = tkinter.Entry(
                self.resultsframe,
                relief='flat',
                bg='white',
                width=50,
                )
        self.results_win_data_1.grid(
                row=1,
                columnspan=1,
                sticky='news')
        self.results_win_data_2 = tkinter.Entry(
                self.resultsframe,
                relief='flat',
                bg='white',
                width=50,
                )
        self.results_win_data_2.grid(
                row=2,
                columnspan=1,
                sticky='news')
        self.results_win_data_3 = tkinter.Entry(
                self.resultsframe,
                relief='flat',
                bg='white',
                width=50,
                )
        self.results_win_data_3.grid(
                row=3,
                columnspan=1,
                sticky='news')
        self.results_win_data_4 = tkinter.Entry(
                self.resultsframe,
                relief='flat',
                bg='white',
                width=50,
                )
        self.results_win_data_4.grid(
                row=4,
                columnspan=1,
                sticky='news')

    # function to grab the data from API based on a query values entered in UI
    def query_npi_api(self):
        print("function triggered")
        # set url of api
        url = "https://npiregistry.cms.hhs.gov/api/"
        query_list = ["?"]
        print(query_list)
        print(self.wildcard_check_status)
        if self.f_name_entry.get():
            if self.wildcard_check_status.get() == 1:
                final_fname_str = 'first_name='+self.f_name_entry.get()+'*'
                query_list.append(final_fname_str)
            else:
                final_fname_str = 'first_name='+self.f_name_entry.get()
                query_list.append(final_fname_str)
            print(query_list)
        if self.l_name_entry.get():
            if self.wildcard_check_status.get() == 1:
                final_lname_str = 'last_name='+self.l_name_entry.get()+'*'
                query_list.append(final_lname_str)
            else:
                final_lname_str = 'last_name='+self.l_name_entry.get()
                query_list.append(final_lname_str)
            print(query_list)
        if self.npi_entry.get():
            final_npi_str = 'npi='+self.npi_entry.get()
            query_list.append(final_npi_str)
            print(query_list)
        if self.state_name_entry.get():
            final_st_name_str = 'state='+self.state_name_entry.get()
            query_list.append(final_st_name_str)
            print(query_list)
        if self.limit_entry.get():
            final_limit_str = 'limit='+self.limit_entry.get()
            query_list.append(final_limit_str)
            print(query_list)
        session = requests.session()
        final_var = str("&".join(query_list))
        print(final_var)
        response = session.get(url+final_var)
        res_json = json.loads(response.text)
        try:
            if res_json['Errors']:
                self.results_win_match_records.config(text='There are no matches to your search')
        except KeyError:
            pass
        if res_json['result_count'] == 1:
            final_dr_txt = '{} {}, {} :: '.format(res_json['results'][0]['basic']['first_name'],
                                                                res_json['results'][0]['basic']['last_name'],
                                                                res_json['results'][0]['basic']['credential'])
            final_npi_text = '{}'.format(res_json['results'][0]['number'])
            final_results_txt = final_dr_txt + '\n' + final_npi_text
            self.results_win_match_records.config(text='There is 1 matching result')
            self.results_win_data_1.insert(0, final_results_txt)
            self.results_win_data_1.config(state='readonly', readonlybackground='white', justify=tkinter.CENTER)
        else:
            self.results_win_match_records.config(text='There are {} matching results'.format(res_json['result_count']))
            if res_json['result_count'] == 2:
                final_dr_txt = '{} {}, {} :: '.format(res_json['results'][0]['basic']['first_name'],
                                                                    res_json['results'][0]['basic']['last_name'],
                                                                    res_json['results'][0]['basic']['credential'])
                final_npi_text = '{}'.format(res_json['results'][0]['number'])
                final_results_txt = final_dr_txt + ' ' + final_npi_text
                self.results_win_data_1.insert(0, final_results_txt)
                self.results_win_data_1.config(state='readonly', readonlybackground='white', justify=tkinter.CENTER)
                final_dr_txt = '{} {}, {} :: '.format(res_json['results'][1]['basic']['first_name'],
                                                                    res_json['results'][1]['basic']['last_name'],
                                                                    res_json['results'][1]['basic']['credential'])
                final_npi_text = '{}'.format(res_json['results'][1]['number'])
                final_results_txt = final_dr_txt + final_npi_text
                self.results_win_data_2.insert(0, final_results_txt)
                self.results_win_data_2.config(state='readonly', readonlybackground='white', justify=tkinter.CENTER)
            elif res_json['result_count'] == 3:
                final_dr_txt = '{} {}, {} :: '.format(res_json['results'][0]['basic']['first_name'],
                                                                    res_json['results'][0]['basic']['last_name'],
                                                                    res_json['results'][0]['basic']['credential'])
                final_npi_text = '{}'.format(res_json['results'][0]['number'])
                final_results_txt = final_dr_txt + ' ' + final_npi_text
                self.results_win_data_1.insert(0, final_results_txt)
                self.results_win_data_1.config(state='readonly', readonlybackground='white', justify=tkinter.CENTER)
                final_dr_txt = '{} {}, {} :: '.format(res_json['results'][1]['basic']['first_name'],
                                                                    res_json['results'][1]['basic']['last_name'],
                                                                    res_json['results'][1]['basic']['credential'])
                final_npi_text = '{}'.format(res_json['results'][1]['number'])
                final_results_txt = final_dr_txt + final_npi_text
                self.results_win_data_2.insert(0, final_results_txt)
                self.results_win_data_2.config(state='readonly', readonlybackground='white', justify=tkinter.CENTER)
                final_dr_txt = '{} {}, {} :: '.format(res_json['results'][2]['basic']['first_name'],
                                                                    res_json['results'][2]['basic']['last_name'],
                                                                    res_json['results'][2]['basic']['credential'])
                final_npi_text = '{}'.format(res_json['results'][2]['number'])
                final_results_txt = final_dr_txt + final_npi_text
                self.results_win_data_2.insert(0, final_results_txt)
                self.results_win_data_2.config(state='readonly', readonlybackground='white', justify=tkinter.CENTER)
            elif res_json['result_count'] == 4:
                final_dr_txt = '{} {}, {} :: '.format(res_json['results'][0]['basic']['first_name'],
                                                                    res_json['results'][0]['basic']['last_name'],
                                                                    res_json['results'][0]['basic']['credential'])
                final_npi_text = '{}'.format(res_json['results'][0]['number'])
                final_results_txt = final_dr_txt + ' ' + final_npi_text
                self.results_win_data_1.insert(0, final_results_txt)
                self.results_win_data_1.config(state='readonly', readonlybackground='white', justify=tkinter.CENTER)
                final_dr_txt = '{} {}, {} :: '.format(res_json['results'][1]['basic']['first_name'],
                                                                    res_json['results'][1]['basic']['last_name'],
                                                                    res_json['results'][1]['basic']['credential'])
                final_npi_text = '{}'.format(res_json['results'][1]['number'])
                final_results_txt = final_dr_txt + final_npi_text
                self.results_win_data_2.insert(0, final_results_txt)
                self.results_win_data_2.config(state='readonly', readonlybackground='white', justify=tkinter.CENTER)
                final_dr_txt = '{} {}, {} :: '.format(res_json['results'][3]['basic']['first_name'],
                                                                    res_json['results'][3]['basic']['last_name'],
                                                                    res_json['results'][3]['basic']['credential'])
                final_npi_text = '{}'.format(res_json['results'][3]['number'])
                final_results_txt = final_dr_txt + final_npi_text
                self.results_win_data_2.insert(0, final_results_txt)
                self.results_win_data_2.config(state='readonly', readonlybackground='white', justify=tkinter.CENTER)
            else:
                self.results_win_match_records.config(text='There are {} matching results.  I can only return max of 4, please narrow your search'.format(res_json['result_count']))
                

    def clear(self):
        self.results_win_match_records.config(text='')
        self.results_win_data_1.config(state=tkinter.NORMAL)
        self.results_win_data_1.delete(0, tkinter.END)
        self.results_win_data_2.config(state=tkinter.NORMAL)
        self.results_win_data_2.delete(0, tkinter.END)
        self.results_win_data_3.config(state=tkinter.NORMAL)
        self.results_win_data_3.delete(0, tkinter.END)
        self.results_win_data_4.config(state=tkinter.NORMAL)
        self.results_win_data_4.delete(0, tkinter.END)
        self.state_name_entry.delete(0, tkinter.END)
        self.l_name_entry.delete(0, tkinter.END)
        self.f_name_entry.delete(0, tkinter.END)
        self.npi_entry.delete(0, tkinter.END)
        self.limit_entry.delete(0, tkinter.END)
        self.wildcard_check.deselect()

if __name__ == '__main__':
    main_window = tkinter.Tk()
    main_window.title('P4 - NPI Registry Search')
    main_window.geometry('425x350')
    app = NPI_API(main_window)
    logging.info('NPI app opened at {}'.format(datetime.datetime.now()))
    main_window.mainloop()
