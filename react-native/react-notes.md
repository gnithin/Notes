## Introduction to ReactJS - Part I

These are notes for this tutorial [here](https://www.codecademy.com/learn/react-101).

### Basics 
- JSX is react's language.
- It needs to be compiled(interpreted right?) into JavaScript.
- It's based on virtual DOM.
- Virtual DOM is basically DOM without it being visually rendered.
- Apparently, since that's the most expensive operation to be done with the DOM, manipulating Virtual DOM is snappier and cleaner. 
- ReactJS basically updates the virtual DOM on every change, diffs it with the current virtual DOM and changes only the required DOM elements. Thereby, making it more efficient. (Don't know if that is true for small pages as well? It seems like a lot of work for simple pages.)

### JSX elements
- Can't use class, it's reserved. Use className in JSX.
- Self-closing tags MUST be added. This is pretty good. No more sloppy tags.
- You can inject javascript into JSX. Use curly braces - {}
- Using the if condn inside the JSX is not possible. There are ways to overcome this - 
  - Use the if outside the JSX. This is the simplest.
  - ternary operator
  - Using the && logical operator
- JSX lists need an attribute called a key. Not exactly sure why it's needed. The explanation is not that clear either. -
    '''
	keys don't do anything that you can see! React uses them internally to keep track of lists. If you don't use keys when you're supposed to, React might accidentally scramble your list-items into the wrong order.

	Not all lists need to have keys. A list needs keys if either of the following are true:

    The list-items have memory from one render to the next. For instance, when a to-do list renders, each item must "remember" whether it was checked off. The items shouldn't get amnesia when they render.

    A list's order might be shuffled. For instance, a list of search results might be shuffled from one render to the next.

	If neither of these conditions are true, then you don't have to worry about keys. If you aren't sure then it never hurts to use them!
    '''
- Everything that JSX does, is basically internally mapped to a function called React.CreateElement(). So basically, JSX is just syntactic sugar.


### JSX Components
- Components are like made-to-order DOM elements, or I should say virtual DOM elements.
- They are re-usable, and are ideally made to do one thing properly.
- They need to be created using the React.createClass(), and need to have an object as an argument with a method - render: function().
- Remember, React.createClass() creates a class. Not an instance. Instance will be created when it's used inside the JSX.
- ReactDOM.render(<component>, ...), calls the render method the of the instance.
- Components names must always be UpperCamelCase.

### Components interactions
- A component instance can actually render another component instance.
- Nesting components this way, is pretty cool, but I think it could make it really complex.

### this.props
- Components can interact by sending arguments to one another.
- It's basically like an attribute for a component, which the component can access using this.props
- All non string props are to be injected through JavaScript - or more simply, just use {}.
- Even event handlers can be passed from the parent component to the child component.
	- I guess it'll be pretty neat to define a default eventHandler to a component, and then if there's an event handler defined by the parent(ie, this.props.eventHandlerName exists), then that can supercede. This is kinda like method overriding (but will probably have to do it manually)
- Naming convention - 
	- Event handlers - handle<EventName>
	- Event attributes - on<EventName>
- On custom components, things like onClick, onHover, don't have any special meaning. Use them as much as you wish.
- getDefaultProps is a method that can be attached to the button for default values of this.props. This where all the default props go.
	- QUESTION - Why does this have to be a method? Why can't it be a simple object? Is it for allowing to perform some kind of computation? How often does that happen?

### this.state
- state is just an object with properties.
- It actually is dynamic in the sense that if there's a change in the state, then wherever it's affected, the component is re-rendered. That's pretty cool.
- You have an initial state defined in the method setInitialState(). And then you can change the state by this.setState({}).
- You can NEVER call this.setState from inside a render function (this.setState will call render internally, therefore, it'll be an infinite loop).

### this.props vs this.state
- this.props should never be changed from within the component. Keep it immutable. The point of this so that other components can talk to the current component through this.props.
- this.state is mutable, since it's used to change state of the component from within itself. You can also allow changing the state by exposing methods to other components which internally change the state. 

## Introduction to ReactJS - Part II
### Passing info from stateful to stateless components.
- A React component should use props to store information that can be changed, but can only be changed by a different component.
- A React component should use state to store information that the component itself can change.
- Using this.funcName from parent to child in React, works the way one thinks it would, and not the way javascripts runs it. It sends a function reference by setting the this to the parent objects method. Refer to the last section here - http://www.digital-web.com/articles/scope_in_javascript/# - The Beauty of Bind.
- Basically it's something like a decorator. The function that's returned is basically just a new function with an .apply call in it. I actually don't understand it fully, but this high level overview is something close I think. But it's really interesting though.
- This is called absolute resolution.(Not really sure about the name)


- So here's a good way to think of this stateless and stateful paradigm in react - 
  - Find out all the different variables on the page
  - Add them as states in a parent stateful component. 
  - Make everything that renders them as stateless components whose parent is that stateful component.
  - Communicate those states from the parent to the child through props.
  - Any change in the state of the parent, will automatically be reflected on the child. 
  - Adv- it's pretty elegant. Cleaner code I suppose, although don't know if this will lead to reduced if-elses. When thinking about it supercially, it should. 

### Advanced react stuff
- Styling - style = {obj} (Use lowerCamelCase for style key values)
- Always have your presentation and the logic components separated.
- Your presentation components are usually just an object with render. You can just write them as a function returning JSX. This is called stateless functional components.
- It can accept props and states as arguments.
- It's more implicit, but apparently this is widely used.

## Proptypes 
- Property types
- `React.propTypes.<type>.?isRequired`
- Can also specify if isRequired or not. 
- Just raises an error on the console if prop does not adhere to the propTypes.
- To add PropTypes to stateless functional components, just create them as it were, and then add the propTypes as a property of the function.

## Forms
- Forms are simple to manipulate in react. 
- Uncontrolled and controlled components - 
  - I am still not 100% sure what these are exactly.
  - An uncontrolled component is a component that maintains its own internal state. -> input tags. It has it's own state.
  - A controlled component is a component that does not maintain any internal state. Since a controlled component has no state, it must be controlled by someone else. So basically, all components
  - In React, when a value is added to an input tag, it becomes controlled(weird). So therefore, it's state needs to be maintained manually. 

## Lifecycle methods
- Basically three categories -
  - mounting - This is only for the first time ever.
    - componentWillMount - Before Component mounts when it's rendered for the first time.
    - render 
    - componentDidMount - After the component is mounted for the first time.
  
  - updating : A component updates every time that it renders, starting with the second render.
    - componentWillReceiveProps - Receives props. Can change the state. 
    - shouldComponentUpdate - Returns boolean to stop or go ahead with the update. You can change the state
    - componentWillUpdate - You cannot change state here. It's basically for non-react setup (window resize etc.)
    - render
    - componentDidUpdate - After rendering is done. Gets the prevProps and prevState (The ones before updating the current ones.)
  
  - unmounting - When component is removed from the DOM
    - componentWillUnmount
		

## Some useful links and their notes
### Regarding [container-component paradigm](https://medium.com/@learnreact/container-components-c0e67432e005#.k9n7g856b)
This is basically separation of logic and visualization.
This tells us that separting things out can actually make the code more reusable, and more importantly, ability to put checks into those smaller modules (I am talking about propTypes)

He basically wrote this blog out of [this talk](https://www.youtube.com/watch?v=KYzlpRvWZ6c). Pretty neat.

### Regarding [setting up ReactJS](https://www.codecademy.com/articles/react-setup-i)
A 5 step process of setting up React.
Man, this is a lot of new stuff. I simply followed the steps. Did not understand how webpack and the rest of them work. Just a high-level overview.
But got it working finally. Might need to go through this multiple times. :P

TODO:
Review these links -
- https://facebook.github.io/react/docs/react-api.html#createelement
- https://facebook.github.io/react/docs/jsx-in-depth.html1
