# Longest Prefix Match

**CHAPTER 09 · VISUAL VOCABULARY**

[Chapter](README.md) · [Forwarding to a destination](01-forwarding.md)

![Three nested route prefixes representing progressively more specific matches.](../../../assets/chapter09-prefix.svg)

*The nested blocks represent ranges. A packet destination can match multiple routes; the most specific matching prefix is selected.*

## Picture words

| No. | Word | Meaning |
| --- | --- | --- |
| 1 | [default route](entries/default-route.md) | A route for destinations with no more specific match. |
| 2 | [destination prefix](entries/destination-prefix.md) | A route covering a range of destination addresses. |
| 3 | [longest prefix match](entries/longest-prefix-match.md) | Selection of the matching route with the greatest prefix length. |

## Examples and usage

> A matching /24 route is selected over a matching /16 route.

> Check for a more specific route before examining the default route.

> Compare route sources only after considering the destination prefix.

> Confirm that the selected route has a reachable next hop.

## More words

[Route metric](entries/route-metric.md) · [Administrative distance](entries/administrative-distance.md) · [Route preference](entries/route-preference.md) · [Equal-cost multipath](entries/equal-cost-multipath.md) · [Recursive route lookup](entries/recursive-route-lookup.md)
0----------------------------------------------9;.llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll/