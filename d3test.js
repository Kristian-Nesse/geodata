<script src="https://d3js.org/d3-contour.v1.min.js"></script>
    <script>

        // Populate a grid of n×m values where -2 ≤ x ≤ 2 and -2 ≤ y ≤ 1.
        var n = 256, m = 256, values = new Array(n * m);
for (var j = 0.5, k = 0; j < m; ++j) {
  for (var i = 0.5; i < n; ++i, ++k) {
            values[k] = goldsteinPrice(i / n * 4 - 2, 1 - j / m * 3);
        }
      }
      
      // Compute the contour polygons at log-spaced intervals; returns an array of MultiPolygon.
      var contours = d3.contours()
          .size([n, m])
          .thresholds(d3.range(2, 21).map(p => Math.pow(2, p)))
          (values);
      
      // See https://en.wikipedia.org/wiki/Test_functions_for_optimization
function goldsteinPrice(x, y) {
  return (1 + Math.pow(x + y + 1, 2) * (19 - 14 * x + 3 * x * x - 14 * y + 6 * x * x + 3 * y * y))
            * (30 + Math.pow(2 * x - 3 * y, 2) * (18 - 32 * x + 12 * x * x + 48 * y - 36 * x * y + 27 * y * y));
      }
      
    </script>