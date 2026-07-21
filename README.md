# ssg

A static site generator written from scratch in Python, with no
third-party dependencies. It walks a directory of Markdown files, converts each
one to HTML using a shared page template, and writes the result to a `docs/`
folder ready to be served or deployed to GitHub Pages.

The Markdown parser is hand-rolled.
Text is tokenized into inline nodes (bold, italic, code, links, images), grouped into
block-level nodes (headings, paragraphs, quotes, lists, code), and
rendered to an HTML node tree that serializes itself to a string.

## Requirements

- Python 3.13+ (see `.python-version` / `pyproject.toml`)
- No runtime dependencies

## Project layout

```text
content/        Markdown source pages (index.md, blog/, contact/)
static/         Assets copied verbatim into the build (CSS, images)
template.html   Page shell; {{ Title }} and {{ Content }} are substituted
config.toml     Build paths (static, content, template, output)
docs/           Generated output (build target)
src/            Source code
main.sh         Local build + preview server
build.sh        Production build for GitHub Pages
test.sh         Run the unit tests
```

## How it works

`src/main.py` drives the build. The source, content, template, and output
paths are read from `config.toml` (`[paths]` table):

1. Clears the output directory and copies everything from `static/` into it.
2. Recursively walks `content/`. For each `.md` file it reads the Markdown,
   converts it to an HTML node tree, extracts the page title from the first
   `# ` heading, injects both into `template.html`, and writes the `.html` file
   to the matching path under `docs/`.

The core modules:

- `textnode.py` — `TextNode` / `TextType`, the inline text model, and
  conversion to leaf HTML nodes.
- `inline_md.py` — inline parsing: delimiter splitting for `**bold**`,
  `_italic_`, inline code, plus image and link extraction.
- `block_md.py` — block parsing: splits Markdown into blocks, classifies each
  (heading, code, quote, unordered/ordered list, paragraph), and builds the
  HTML tree.
- `htmlnode.py` — `HTMLNode`, `LeafNode`, `ParentNode` and their `to_html()`
  serialization.
- `generate_content.py` — page generation, title extraction, and the recursive
  content walk.

## Usage

Build the site (output goes to `docs/`, base path `/`):

```bash
python3 src/main.py
```

Build for GitHub Pages under a repository subpath (rewrites root-relative
`href="/`/`src="/` to the given base path):

```bash
./build.sh          # builds with basepath "/ssg/"
```

The base path is the first CLI argument, defaulting to `/`:

```bash
python3 src/main.py "/my-repo/"
```

To preview locally, build and serve the `docs/` folder with `main.sh`:

```bash
./main.sh           # builds, then serves docs/ at http://localhost:8888
```

## Supported Markdown

- Headings (`#` through `######`)
- Paragraphs
- Bold (`**text**`), italic (`_text_`), and inline code spans
- Links (`[text](url)`) and images (`![alt](url)`)
- Blockquotes (`>`)
- Unordered lists (`- `) and ordered lists (`1. `, `2. `, …)
- Fenced code blocks (triple backticks)

**Limitation**: No current support for nested elements (e.g. bold inside italic is not parsed).

## Tests

```bash
./test.sh           # python3 -m unittest discover -s src
```

## License

MIT - see [LICENSE](LICENSE).
