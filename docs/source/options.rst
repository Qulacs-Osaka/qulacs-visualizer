.. _how_to_use_options:

===========================
How to use options
===========================

This section explains how to use the options available in circuit_drawer.

******************
Text-Based Drawing
******************

-------------------
Numbering the gates
-------------------

Set ``verbose`` to ``True``. (Default: ``verbose=False``)

>>> circuit_drawer(circuit, output_method='text', verbose=True)
   ___     ___     ___
  | X |   |DeM|   |CX |
--|000|---|003|---|004|----------
  |___|   |   |   |___|
   ___    |   |     |
  | Y |   |   |     |
--|001|---|   |-----|------------
  |___|   |___|     |
   ___              |      ___
  | Z |             |     | X |
--|002|-------------●-----|005|--
  |___|                   |___|

----------------------------
Change the control dot style
----------------------------

In default, character "●" is used to mean control qubit. But in CommandPrompt, sometimes display layout is corrupted.
In this case, please use the character "."(``dot="small"``) instead of the character "●"(``dot="large"``).

Use the ``dot``. ``large`` and ``small`` are available. (Default: ``dot="large"``)

>>> circuit_drawer(circuit, output_method='text', dot="small")
   ___     ___     ___
  | X |   |DeM|   |CX |
--|   |---|   |---|   |----------
  |___|   |   |   |___|
   ___    |   |     |
  | Y |   |   |     |
--|   |---|   |-----|------------
  |___|   |___|     |
   ___              |      ___
  | Z |             |     | X |
--|   |-------------･-----|   |--
  |___|                   |___|


******************
Matplotlib Drawing
******************

-----------------
Change image size
-----------------

Use the ``dpi``, ``scale`` option to change the image size. (Default: ``dpi=72``, ``scale=0.6``)
In most cases, use ``scale``, but adjust the ``dpi`` if you want to generate a sharper image.

>>> circuit_drawer(circuit, output_method='mpl', dpi=72, scale=0.6)

*************
LaTeX Drawing
*************

**The LaTeX drawing function is currently under implementation and may not work correctly.**

-----------------
Change image size
-----------------

Use the ``ppi`` option to change the image size. (Default: ``ppi=150``)

>>> circuit_drawer(circuit, output_method='latex', ppi=150)
