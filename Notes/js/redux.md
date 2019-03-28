# Redux basics

Notes for understanding redux basics. I am following [this book](https://medium.freecodecamp.org/understanding-redux-the-worlds-easiest-guide-to-beginning-redux-c695f45546f6), it's pretty comprehensive and I'd really really recommend it to anyone starting out with redux (but knows react)

- Redux is fundamentally a state-manager. That's it. It is a stream-lined way to manage state and transform them for a given action.
- Some basic rules(or principles mentioned in the book) of redux - 
    - One application state object managed by one store
        - Create one store, and use it everywhere
    - The only way to change the state is to emit an action, an object describing what happened
    - To specify how a state-tree is transformed, you write pure reducers.
        - I don't understand why the word state-tree is being used instead of state-object or just state.
        - I don't understand what's a 'pure' reducer? I though reducer was just a function

- Basic redux elements involve - 
    - Store - The store. You can create one using `createStore(reducer, initialState)`
    - Action - An object with meta-data.
    - Reducer - A function that transforms a state based on the actions given. It can also contain an initial-state.

- The `createStore` returns an object that has 3 methods 
    - getState() - returns the current state 
    - subscribe(listener) - Allows a listener-callback whenever a dispatch operation happens. It returns an object, which can be used to unsubscribe a listener
    - dispatch(action) - Passes the action and the current state to the reducer and calls all the listeners, every-time it's dispatched.
    - Check out the blog for the source-code that explains this

- Usually has a `type` and a `payload`
    - For example - 
        ```
        {
            type: "SET_TECHNOLOGY",
            text: "Elm"
        }
        ```
    - Note that types are usually in capitals

- Action Creators are simply functions that help you create actions. That’s all. They are functions that return action objects.

- Never Mutate State Within the Reducers.
    - This seems to be advice, but not really sure the reason is given. I guess this is from a functional-programming model of thinking.
    - This is probably because of this - 
        ```
        https://github.com/reduxjs/redux/pull/1289#issuecomment-175617759
        ```
    - This is because redux assumes that the state returned is a brand new one. Hence, it'll be easier to check for state changes this way. If there is no change, then the state reference remains the same. If there is a state change, then the reference would entirely be different. Hence doing this is a way to simplify the code and it's reasoning (especially in js).

- An action creator is nothing but a function that returns an object with the action-type and the payload (from the function args)

- You can have multiple reducers, which can be used with `combineReducers`
    - This is pretty useful I guess
    - This will make the life easy for whenever the state object is too complex
