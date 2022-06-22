"""
Handles the connection to Digiclear server and sets the correct urls to access
the API (depending on whether it is digiclear (default) or remoteclear (for tests).
Thanks to C. Villebasse for the login code snippet. 
"""

import requests
import lxml.html

class DigiclearConnection():
    
    def __init__(self, servername = 'digiclear'):
        """
        This class should handle connection to Digiclear (or Remoteclear) and set the correct 
        url to reach the API

        Parameters
        ----------
        servername : str, optional
            Name of the digiclear server, to choose between 'digiclear', 'remoteclear' 
            or 'remoteclear-lan' depending on where you are. The default is 'digiclear'.

        Returns
        -------
        None.

        """
        self.login_url = f'https://sso.u-psud.fr/cas/login?service=https%3A%2F%2F{servername}.c2n.u-psud.fr%2Flogin'
        self.base_url = f'https://{servername}.c2n.u-psud.fr/'
        self.base_api_url = f'https://{servername}.c2n.u-psud.fr/api/'
        
        self.s = requests.session() ## opens a session
    
    def login(self, username, password, check_certificate=True):
        """
        Login to the digiclear server indicated during instanciation

        Parameters
        ----------
        username : str
            username for the connection. firstname.lastname
        password : str
            password for the username. NOT encrypted whatsoever.
        check_certificate : bool
            boolean to check that the certificate matches or not. 
            Ultimately this should disappear, but remoteclear-lan returns an error because 
            it does not match the certificate name (remoteclear).
        
        Returns
        -------
        None.

        """
        login = self.s.get(self.login_url) ## get all the text from the url. This is a binary object
        login_html = lxml.html.fromstring(login.text) ## decode the text from the response above and parse to produce html element
        hidden_inputs = login_html.xpath(r'//input[@type="hidden"]') ## makes a XPath query. XPath navigates through elemnts in a XML doc
        form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs[:2]}
        form['username']=username
        form['password']=password
        response = self.s.post(self.login_url, data=form, verify=check_certificate)
        if response.url != self.base_url:
            print('Login failed')
            success = False
        else:
            success = True
        return success
        
    def disconnect(self):
        """ closes the connection"""
        self.s.close()
        
