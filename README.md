# IoT_VSaas
vsaas survellance detection

## Known issue (macOS + external monitors)

When running via OpenCV `cv2.imshow` on macOS, moving the preview window to a different/extended monitor may cause the preview window to disappear while the terminal process keeps running.

Current workaround:
- Keep the OpenCV preview window on the same display where it was first opened.
- If the window disappears, stop and restart the script.
