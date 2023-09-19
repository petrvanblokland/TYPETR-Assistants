

    '''
    def drawGlyphErrors(self, glyph, errors, x, y):
        """Shows bounding box in red, if there are any errors with the current
        glyph."""
        # TODO: analyzer doesn't support other types besides DoodleFont?
        if isinstance(self.style, Style) and isinstance(self.style.storage, OTFStorage):
            if self.otfWarning is False:
                errors.append('Warning: GlyphAnalyzer not implemented for OTFStorage yet!')
                self.otfWarning = True
        else:
            errors = self.checkGlyph(glyph)

            if self._showErrors and errors:
                _, h, _ = self.getPaperSize()
                stroke(None)
                fill(1, 0.7, 0.7)
                w = glyph.width * self.scale
                rect(x, h - y - self.descender, w, self.size)

            # Copies all errors of this glyph into the caller's error pool.
            for error in errors:
                print(error, type(error))
                self.errors.append(error)
    '''

    '''
    def drawGlyphBitmap(self, glyph, x, y, doBitmap):
        """Draws the glyph bitmap representation.

        TODO: untested.
        """
        if not doBitmap:
            return

        w, h, _ = self.getPaperSize()
        bitmapAndOffset = self.getGlyphBitmap(glyph, self.scale)

        if bitmapAndOffset is not None:
            bitmap, (offsetX, offsetY) = bitmapAndOffset
            scaledBitmap = self.resizeBitmap(bitmap, self.zoom)
            data = bitmap.TIFFRepresentationUsingCompression_factor_(NSTIFFCompressionNone, 0.0)

            # Writes TIFF bitmap representation to files. Enable for testing.
            #data.writeToFile_atomically_('/Users/michiel/%s.tiff' % glyph.name, False)

            # DrawBot scale() method; seems to generate rounding errors.
            originalX = x + offsetX * self.scale - margin + margin / zoom
            originalY = h / zoom - y + (offsetY * self.scale) + margin - margin / zoom
            save()
            scale(zoom)
            image(bitmap, (originalX, originalY))
            restore()
            #scale(1/zoom)

            # Resized bitmap method.
            originalX = x + offsetX * self.scale
            scaledX = getZoomed(originalX, self.margin, self.zoom)
            scaledY = h - getZoomed(y - offsetY * self.scale, self.margin, self.zoom)
            image(scaledBitmap, (scaledX, scaledY))
    '''

    '''
    def resizeBitmap(self, bitmap, zoom):
        """Resizes bitmap without interpolation so we can blow up antialiasing
        pixels."""
        # TODO: move to proofing.tx
        w, h = bitmap.size()

        if w == 0 and h == 0:
            return bitmap

        width = w * zoom
        :eight = h * zoom
        sourceFrame = NSMakeRect(0, 0, w, h)
        targetFrame = NSMakeRect(0, 0, width, height)
        targetImage = NSImage.alloc().initWithSize_((width, height))
        targetImage.lockFocus()
        hints = {NSImageHintInterpolation: NSImageInterpolationNone}
        bitmap.drawInRect_fromRect_operation_fraction_respectFlipped_hints_(targetFrame,
                sourceFrame, NSCompositeCopy, 1.0, True,
                hints)
        targetImage.unlockFocus()
        return targetImage
    '''

