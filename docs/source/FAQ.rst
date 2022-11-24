.. default-domain:: py

.. _faq:

Frequently Asked Questions
===========================

Can I loose / corrupt data if the software crashes, or malfunctions ?
----------------------------------------------------------------------

Short answer: No.
This program reads the JSON file downloaded from Digiclear, and simply retrieves additional data (machine names, etc.). Thus, it only *reads* data from Digiclear, and cannot in any way temper with what is on the database. Your sample data is safe.

Why do I need to enter my login/password ?
------------------------------------------

If you open the sample history JSON file, you will see that some information is missing. For example, at any process step the machine on which the operation was performed is indicated as::

    "machineId": XXXX

where :code:`XXXX` is the unique id number of the machine in the Digiclear database. The program thus needs to connect to Digiclear to retrieve this information. This is done through an `API <https://en.wikipedia.org/wiki/API>`_, and you can actually read Digiclear's API `here <https://clearwiki.c2n.u-psud.fr/doku.php?id=digiclear:admin#api_sexchanging_data_with_digiclear>`_.
Some of the information can be restricted to the sample owner(s). Hence the necessity to login. The login interface is still the same, and is provided by UPSaclay's Central Authentication Service (CAS). All of this should, in principle, be safe.

The PDF looks bad. What can we do about it ?
---------------------------------------------

Developping this type of add-ons takes time. A number of improvements could be made. Here are some things in no particular order:
* Adding a docx or odt export format (see e.g. `<https://python-docx.readthedocs.io/en/latest/>`_ or `<https://github.com/eea/odfpy>`_.
* Contributing to the PDF export module by suggesting layouts or developping another one.
