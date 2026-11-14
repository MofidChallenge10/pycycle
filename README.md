# PyCycle

Explain circular imports in a Python package using the standard-library AST parser.

```bash
python -m pip install .
pycycle src/
pycycle --json .
```

The analyzer maps imports to modules found under the supplied root. It does not resolve installed third-party packages or execute project code. Dynamic imports are not detected.

## Tests
```bash
python -m unittest discover -s tests -v
```

MIT.
