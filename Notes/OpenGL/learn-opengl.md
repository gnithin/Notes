# Learning OpenGL

Source - https://learnopengl.com/Getting-started/OpenGL Amazing site!

## Basics 
- https://learnopengl.com/Getting-started/OpenGL
- OpenGL is a state-machine.
- We interact with the state using OpenGL context.
- When working in OpenGL we will come across several state-changing functions that change the context and several state-using functions that perform some operations based on the current state of OpenGL. As long as you keep in mind that OpenGL is basically one large state machine, most of its functionality will make more sense.
- Object is an abstraction, representing the a subset of OpenGL's state.
- An Object is like a struct with properties.


### Understanding SDL
- Since drawing a window and taking in user-inputs differs from hardware to hardware, OpenGL does not get into the specifics of that. It purposefully makes it abstract so that the user can use a library according to their OS/platform.
- This means we have to create a window, define a context, and handle user input all by ourselves.
- This is where SDL comes in -

- SDL - https://www.libsdl.org/
	- It's a library to handle creating a window, defining an OpenGL context and handle user inputs from keyboard and mouse.
	- Simple DirectMedia Layer is a cross-platform development library designed to provide low level access to audio, keyboard, mouse, joystick, and graphics hardware via OpenGL and Direct3D.

- [QUESTION] I don't really understand the difference between context and object
	- There can only be one context in OpenGL, while it can have a lot objects
	- You can create an object, set some options, and then bind/unbind to openGL context, whenever I want.

- When using SDL, use SDL to create a window, create an OpenGL context, and bind that to the window

### Understanding GLAD
- I never really understood the point of GLAD
- OpenGL is a spec, it's a standard. So basically, different graphics-card manufacturers (I am not talking about accelerated graphics cards, but the default ones that every machine has) have the liberty to follow the spec and place the code wherever they want.
- So in order to use the OpenGL functions, my program needs to find where it's located.
- This is why we need glad - https://github.com/Dav1dde/glad
- On a high level, I think it basically loads and links OpenGL code, depending on the version and the hardware type
- We need to generate different GLAD files for different languages, and different versions of OpenGL standards (Do all graphics card implement all OpenGL standards?)
- This we can do from this website, which is pretty freaking cool - https://glad.dav1d.de/

- [QUESTION] What's the difference between a Buffer and an Object?

- Note that processed coordinates in OpenGL are between -1 and 1
- OpenGL has state-setting functions and state-using functions.
	- One configures the state, while the other actually uses the state vars to do something
	- Example - 
	  ```
	  glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
	  glClear(GL_COLOR_BUFFER_BIT);
	  ```


## Hello Triangle 
- https://learnopengl.com/Getting-started/Hello-Triangle
- The graphics pipeline can be divided into two large parts: the first transforms your 3D coordinates into 2D coordinates and the second part transforms the 2D coordinates into actual colored pixels.

- Shaders are small programs that run in the GPU
- Each program that is run is part of the pipeline

- The graphics pipeline 
	- A set of states before drawing a shape on the screen
	- From the CPU, we passing in the data coordinates into the shaders, which are all run in the GPU
	- Main shaders are vertex and fragment
	- Shaders work pixel by pixel (Or position by position )
	- Vertex shader - Takes in a 3d coord and returns a new 3d coord
		- I honestly never understood the significance of this
		- I think i
	- Fragment shader - Applies a color to the current vertex being processed

- With the vertex data defined we'd like to send it as input to the first process of the graphics pipeline: the vertex shader. This is done by creating memory on the GPU where we store the vertex data, configure how OpenGL should interpret the memory and specify how to send the data to the graphics card. The vertex shader then processes as much vertices as we tell it to from its memory. 
	-  We manage this memory via so called vertex buffer objects (VBO) that can store a large number of vertices in the GPU's memory. The advantage of using those buffer objects is that we can send large batches of data all at once to the graphics card, and keep it there if there's enough memory left, without having to send data one vertex at a time. Sending data to the graphics card from the CPU is relatively slow, so wherever we can we try to send as much data as possible at once. Once the data is in the graphics card's memory the vertex shader has almost instant access to the vertices making it extremely fast 

- OpenGL allows us to bind to several buffers at once as long as they have a different buffer type.

- Using a buffer - 
	- You generate a buffer, attach it to an ID internally using glGenBuffer()
	  ```
	  unsigned int VBO;
	  glGenBuffers(1, &VBO);
	  ```
	- Then you bind the buffer to a specific type - 
	  ```
	  glBindBuffer(GL_ARRAY_BUFFER, VBO);  
	  ```
	- Now whenever we refer to GL_ARRAY_BUFFER, we are talking about this binding
	  ```
	  glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
	  ```

- I really did not understand the requirement of Vertex array objects, other than the face that core OpenGL won't draw anything without it :( 


