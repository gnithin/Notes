### Understanding flexbox

This is from [this awesome CSSTricks blog](https://css-tricks.com/snippets/css/a-guide-to-flexbox/).

- Flexbox tries to be the replacement for `display: inline/block` and using `Table` tag.
It basically can be used when the size of the container is not known in advance. 
- Pretty cool in the sense that it tries mimic the positioning in native (it sure feels that way).
- Important thing to remember is that it has a main axis (based of the `flex-direction`) and a cross axis. Everything property is based off of this. 
- Also, there is a gentle note that says - Use [Grid View](https://css-tricks.com/snippets/css/complete-guide-grid/) for heavy duty stuff. Not reading that right now :p

There are basically 2 types of the styling properties based on where it's used - in the parent container and the child container.

These are the important properties in the parent - 
- `display`: Making it `flex` makes the parent basically flex controlled. There is no observable affect on the elements.
- `flex-direction`: This specifies the direction of the main-axis of the children contained. It also has the reverse counterparts as well.
- `flex-wrap`:  By default, flex will NOT wrap. You need to add wrapping explicitly.
- `justify-content`: It defines the positioning of children in the main axis, after the full length of the children are set. It does NOT resize the children. Just their positioning and the size between them.
- `align-items`:  It defines the positioning of the children in the cross axis (within a single line). It can change the size of the individual child.
- `align-content`:  This basically tries to positioning the spacing between multiple lines in the cross axis. It can redistribute the elements based on the empty space left after the elements have reached their full size. NOTE: It has NO effect when there's a single line in the cross axis.

These are the important properties for the children -
- `order`: This changes the order of the children. NOTE: By default, all the flexible items are set to an order of 0, which is the default order. If you want to bring one element to front or something simple like that, You can use -ve numbers to avoid setting order to all the elements.
- `align-self`: This overrides the behaviour as specified by `align-items`. It works on the cross axis. It can be pretty useful in situations where you need to change only one item among the rest.
- `flex`: This accepts a number that can be used to size the current set of elements proportionally. NOTE: This is not exactly the meaning of this. Refer the original text for it's correct meaning. But you will use it the way that I've specified.

NOTE: `float`, `clear` and `vertical-align` have no effect on a flux item (Both the parent and the child)