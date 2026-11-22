# Python learning materials

This package is generated from the supplied `learning_material_resource_mapping.csv`. It contains one course only: Programming → Python, with 16 topic entries.

## Structure
- `resource_index.csv`: topic metadata, original PDF/YouTube links, and paths to lesson files.
- `source_csv_original.csv`: unchanged source CSV copy.
- `programming/python/topics/<topic_id>/lesson.md`: starter lesson template for each topic.
- `programming/python/topics/<topic_id>/resources/`: place downloaded PDFs or other approved local resources here.

## Important checks
- All 16 rows currently have a PDF link and YouTube link.
- The supplied YouTube URL is repeated across all topics (with whitespace differences in the CSV). Verify that it is relevant to each topic before showing it to learners.
- PDF links are external Google Drive links; they are not downloaded into this package. Check access permissions and topic relevance.
- Lesson files are templates, not completed instructional content.
- Keep course IDs and topic IDs unchanged. Do not modify assessment question banks as part of this task.

## Integration
Add this `learning_material/` directory at the repository root, alongside `courses/`, `backend/`, and `frontend/`. Backend should read the index and serve the relevant lesson/resource to the frontend. Coordinate the API contract with the backend owner before changing APIs or schemas.
