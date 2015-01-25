# pdfslicer
Tool for slicing a pdf document page into several smaller pages.

	Usage: pdfslicer inputfile.pdf [Options]
		Options:
		-p page		Choose which page to slice
		-s 			Print dimensions of inputfile
		-d			Dry-run
		-o output		Output file name
		-O orientation	Choose page orientation (l for landscape, p for portrait)
		-P papersize	Choose output paper size (A6, A5, A4, A3, A2, A1, A0)

**Planned features**:
- Multi page support;
- Margins and offsets;
- Custom page sizes;
- Slicing by bounding box in several pages;
