# `vizelec`

**Usage**:

```console
$ vizelec [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `pinout`
* `schem`: Create a graph representation of the...

## `vizelec pinout`

**Usage**:

```console
$ vizelec pinout [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `show`

### `vizelec pinout show`

**Usage**:

```console
$ vizelec pinout show [OPTIONS] CONF_FILE
```

**Arguments**:

* `CONF_FILE`: [required]

**Options**:

* `--help`: Show this message and exit.

## `vizelec schem`

Create a graph representation of the schematic given by schem.
:param schem: path to a spice file.

**Usage**:

```console
$ vizelec schem [OPTIONS] SCHEM
```

**Arguments**:

* `SCHEM`: [required]

**Options**:

* `--help`: Show this message and exit.
