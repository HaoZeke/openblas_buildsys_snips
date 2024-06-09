;; Emacs script to clean and convert all Org mode files in docs/source to Markdown without generating TOC

(defun my-org-md-export-to-markdown-no-toc ()
  "Export the current Org buffer to a Markdown file without a TOC."
  (let ((org-export-with-toc nil))
    (org-md-export-to-markdown)))

(defun convert-org-files-to-md ()
  "Convert all Org files in the 'docs/source' directory to Markdown without generating TOC."
  (let ((default-directory (expand-file-name "docs/source")))
    (dolist (file (directory-files-recursively default-directory "\\.org$"))
      (with-current-buffer (find-file-noselect file)
        (let ((output-file (concat (file-name-sans-extension file) ".md")))
          (my-org-md-export-to-markdown-no-toc)
          (rename-file (concat (file-name-sans-extension file) ".md") output-file t)
          (kill-buffer))))))

(defun clean-md-files ()
  "Remove Markdown files that have corresponding Org files in the 'docs/source' directory."
  (let ((default-directory (expand-file-name "docs/source")))
    (dolist (file (directory-files-recursively default-directory "\\.org$"))
      (let ((md-file (concat (file-name-sans-extension file) ".md")))
        (when (file-exists-p md-file)
          (delete-file md-file)
          (message "Deleted file: %s" md-file))))))

(defun clean-and-convert-org-files-to-md ()
  "Clean Markdown files that have corresponding Org files and convert all Org files to Markdown without generating TOC."
  (interactive)
  (clean-md-files)
  (convert-org-files-to-md))

;; Run the clean and conversion function
(clean-and-convert-org-files-to-md)
