# Open Tracer v0.1 (very) alpha

Should be considered a simple proof-of-concept only.

## Conception
I happened across [a TikTok video](https://www.tiktok.com/@morleykert/video/7331777662664363269) from Morley Kert in which he used a [Shaper Trace](https://www.shapertools.com/en-us/trace) to quickly scan a hand sketch into a vector format which he then used for modelling and 3d printing.  While I liked the product, I wanted to play around with the concept immediately and had something akin to the [Hacker News Dropbox moment](https://news.ycombinator.com/item?id=9224) and thought I could probably do something similar with a little hacking around in Python.

## Concept
1.  Create [a page](https://github.com/Tom1827/open_tracer/blob/main/page%20v2.pdf) with QR codes placed at known locations (which can be printed out).
2.  Draw a design on that page, and take a photo of it at a decent resolution.
3.  Analyse the page with [pyzbar](https://github.com/NaturalHistoryMuseum/pyzbar/tree/master), returning the QR code locations
4.  Use [pillow](https://github.com/python-pillow/Pillow) to perform a perspective transform using the QR code locations, effectively straightening the image (removing any perspective skew introduced when the photograph was taken).
5.  Use [pyautotrace](https://github.com/lemonyte/pyautotrace) to trace the straightened image, and then output the resulting vector in a couple of useful vector formats.

Thanks to the wonderful strength of the Python ecosystem, this works and took only a handful of lines of code.

## Test example
* Download test.jpg and open_tracer.py into the same folder.
* Make sure that the dependences are installed (pyzbar, autotrace, pillow, and [numpy](https://github.com/numpy/numpy))
* Run `python open_tracer.py test.jpg`
* All being well, traced DXF and SVG should be created.

## Tracing your own drawing
* Download and print out page v2.pdf **without scaling**.  Note that one of the shorter sides of the resultant print had a slightly larger margin.  It's A4 only currently - sorry.
* Draw something on the page.
* Placing the page in landscape, and the larger margin to the right, take a careful and clear picture of the page.
* Copy that image file into the folder with open_tracer.py, and run `python open_tracer.py <yourfile.jpg>`

## Notes
* This is very alpha, proof-of-concept code.  There's virtually no error checking, and probably myriad ways to break it.  I've only tested it on Windows; YMMV.
* In particular, at present there's no accounting for different rotations of the page, and thus different positioning of the QR codes.  The printable page has a larger margin along one of the shorter sides (i.e. the bottom, as printed) to account for the wider print area margin there on most printers.  Put this part of the page to the right (and therefore in landscape) as you photograph it.  What it really needs is to be on the right in the final image, so you could also rotate the image aftwards.  Your call.
* The photo needs to be clear, as pyzbar needs to recognise all four QR codes.  I had issues making this work reliably with an iPhone 13 Pro and 1 cm QR codes, so I increased them to 1.5 cm which seems to be much better.
* Currently, with the page laid out as described above, the scanned area will be the area surrounded by the *inner* corners of the QR codes, so 24cm by 16cm.
* The output dimensions seem pretty accurate, although annoyingly they're output in tenths of a millimeter, so you might need to do a little scaling.
* The default tracing approach is to trace both sides of a thin line; if you're modelling from the created vector, you'll probably want to choose one of the sides and delete the other.

## Possible future to-dos
* Fix the rotation issue so any orientation of image will work.
* Make the output units sensible.
* Add a US letter page (and maybe other page sizes?) with different QR codes which would automate setting different dimensions.
* A simple mobile app automating all of the above would be slick - I wonder how the Python-iPhone ecosystem would support this?  ([Flet](https://flet.dev/) didn't support cameras when I last checked; obviously there are other options too, but Flet is quite nice for simple apps.)
