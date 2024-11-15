Documenting Code in reStructuredText for Sphinx
================================================

Introduction
------------
Sphinx supports automatic code documentation using the ``autodoc`` extension, which extracts docstrings from your code and integrates them into your documentation. This guide explains how to structure your code comments using reStructuredText to ensure your documentation is well-formatted and informative.

1. Setting Up the Documentation
-------------------------------
Before you start documenting, make sure you have the Sphinx project and ``autodoc`` enabled in your ``conf.py``::

    # In conf.py, ensure these extensions are present
    extensions = [
        'sphinx.ext.autodoc',
        'sphinx.ext.napoleon',  # Optional: For Google/NumPy style docstrings
    ]

2. Writing Docstrings with reStructuredText
-------------------------------------------
reStructuredText is a lightweight markup language used in docstrings. Here’s how to write effective docstrings for different parts of your code.

**2.1 Module-Level Docstring**

At the top of your module (``mymodule.py``), include a general description::

    """
    mymodule.py
    ===========

    This module contains functions and classes for data processing.
    """

**2.2 Documenting Functions**

Describe the function’s purpose, parameters, and return values. Use the following format::

    def add_numbers(a, b):
        """
        Adds two numbers together.

        :param int a: The first number.
        :param int b: The second number.
        :returns: The sum of `a` and `b`.
        :rtype: int
        """
        return a + b

**2.3 Documenting Classes**

For classes, include a class-level docstring and document each method::

    class Calculator:
        """
        A simple calculator class to perform basic arithmetic operations.

        :param str name: The name of the calculator instance.
        """

        def __init__(self, name):
            """
            Initializes the calculator with a given name.
            """
            self.name = name

        def multiply(self, x, y):
            """
            Multiplies two numbers.

            :param int x: The first factor.
            :param int y: The second factor.
            :returns: The product of `x` and `y`.
            :rtype: int
            """
            return x * y

**2.4 Documenting Class Attributes**

Use the ``:ivar`` directive to describe class attributes::

    class Rectangle:
        """
        Represents a geometric rectangle.

        :ivar float length: The length of the rectangle.
        :ivar float width: The width of the rectangle.
        """
        def __init__(self, length, width):
            self.length = length
            self.width = width

3. Formatting Docstrings
------------------------
**3.1 Sections**

Use specific section headers (optional but recommended):

- ``Parameters``
- ``Returns``
- ``Raises`` (for exceptions)

Example::

    def divide(x, y):
        """
        Divides `x` by `y`.

        **Parameters:**

        - `x (float)`: Numerator.
        - `y (float)`: Denominator.

        **Returns:**

        - `float`: The result of division.

        **Raises:**

        - `ZeroDivisionError`: If `y` is zero.
        """
        if y == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return x / y

**3.2 Cross-referencing**

To reference other parts of the code, use the ``:class:``, ``:func:`` and similar directives::

    """
    See also :class:`Calculator` for more operations.
    """

4. Building the Documentation
-----------------------------
Once your code is documented, build the documentation to see the results::

    make html

This will generate the HTML files in the ``_build`` directory, integrating your code comments into the documentation.

5. Cleaning the Build Directory
-------------------------------
If you need to rebuild the documentation from scratch, use::

    make clean

This removes all previously built files.
