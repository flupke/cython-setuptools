# History

## 0.2.3

- extract_args() handles missing args.

## 0.2.2

- pkg-config -L, -l and -I flags are extracted and put in modules'
  library_dirs, libraries and include_dirs respectively.

## 0.2.1

- Use Cython's cythonize() instead of deprecated build_ext.
- Python 3 unicode fix.
- Defaults section extra fields are now merged in module dicts.

## 0.2

- Unrecognized fields are also included in `parse_setup_cfg()`'s module dicts.

## 0.1

- First public release.
