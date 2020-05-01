#include <stdio.h>
#include <stdbool.h>

#include <SDL.h>
#include <GL/gl.h>
#include <GL/glu.h>

// #include "engine_sdl.h"

SDL_Window* main_window = NULL;

/* Destroy */
void engine_sdl_quit()
{
    SDL_Quit();
}
void engine_sdl_destroy_window(SDL_Window** window, SDL_GLContext glcontexte)
{
    SDL_DestroyWindow(*window);
    SDL_GL_DeleteContext(glcontexte);
}

// SDL and OPENGL INIT
bool engine_sdl_init()
{
    if (SDL_Init(SDL_INIT_VIDEO != 0))
    {
        engine_sdl_quit();
        return false;
    }

    return true;
}

bool engine_sdl_create_window(SDL_Window** window, SDL_GLContext glcontexte, int width, int height, char* title)
{
    *window = SDL_CreateWindow(title,
                              SDL_WINDOWPOS_UNDEFINED,
                              SDL_WINDOWPOS_UNDEFINED,
                              width,
                              height,
                              SDL_WINDOW_OPENGL|SDL_WINDOW_RESIZABLE);
    if (*window == NULL)
    {
        SDL_Quit();
        return false;
    }
    SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 1);
    SDL_GL_SetAttribute(SDL_GL_DEPTH_SIZE, 24);

    glcontexte = SDL_GL_CreateContext(*window);
    if (glcontexte == NULL)
    {
        SDL_Quit();
        return false;
    }

    // sync buffer swap with monitor's vertical refresh rate
    SDL_GL_SetSwapInterval(1);

    return true;
}

bool init_gl(GLvoid)
{
    glShadeModel(GL_SMOOTH); // ombrage

    glClearColor(0.0f, 0.0f, 0.0f, 0.0f);

    glClearDepth(1.0f); // buffer
    glEnable(GL_DEPTH_TEST); // test
    glDepthFunc(GL_LEQUAL);

    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST);

    return true;
}

GLvoid resize_window(GLsizei width, GLsizei height)
{
    GLfloat ratio;

    if (height == 0) // no divide by 0
    {
        height = 1;
    }
    glViewport(0, 0, width, height);

    ratio = width / height;

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    gluPerspective(45.0f, ratio, 0.1f, 100.0f);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
}

// my test function
bool draw_scene(GLvoid)
{
    // fps
    static GLint t0     = 0;
    static GLint frames = 0;

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glLoadIdentity(); // remettre à zéro


    /*glTranslatef(-1.5f, 0.0f, -6.0f);

    glBegin(GL_TRIANGLES);
        glVertex3f( 0.0f,  1.0f, 0.0f);
        glVertex3f(-1.0f, -1.0f, 0.0f);
        glVertex3f( 1.0f, -1.0f, 0.0f);
    glEnd();

    glTranslatef(3.0f, 0.0f, 0.0f);
*/
    glTranslatef(1.5f, 0.0f, -6.0f);
    glBegin(GL_QUADS);
        glVertex3f(-1.0f,  1.0f, 0.0f);
        glVertex3f( 1.0f,  1.0f, 0.0f);
        glVertex3f( 1.0f, -1.0f, 0.0f);
        glVertex3f(-1.0f, -1.0f, 0.0f);
    glEnd();

    /* Draw it to the screen */
    SDL_GL_SwapWindow(main_window);
    frames++;
    {
        GLint t = SDL_GetTicks();
        if (t - t0 >= 5000)
        {
            GLfloat seconds = (t - t0) / 1000.0;
            GLfloat fps = frames / seconds;
            printf("%d frames in %g seconds = %g FPS\n", frames, seconds, fps);
            t0 = t;
            frames = 0;
        }
    }

    return true;
}

int main(int N, char* T[])
{
    bool quit = false;
    bool visible = true;
    SDL_GLContext glcontexte = NULL;
    SDL_Event event;

    if (engine_sdl_init() == false)
    {
        return 1;
    }

    if (init_gl() == false)
    {
        engine_sdl_quit();
    }

    if (engine_sdl_create_window(&main_window, &glcontexte, 640, 480, "Nehe") == false)
    {
        return 1;
    }
    /* resize the initial window */
    resize_window(640, 480);

    while (quit == false)
    {
        while (SDL_PollEvent(&event))
        {
            switch (event.type)
            {
                case SDL_WINDOWEVENT:
                    switch(event.window.event)
                    {
                        case SDL_WINDOWEVENT_RESIZED:
                            /* handle resize event */
                            resize_window(event.window.data1, event.window.data2);
                            break;
                        case SDL_WINDOWEVENT_HIDDEN:
                            visible = false;
                            break;
                        case SDL_WINDOWEVENT_SHOWN:
                            visible = true;
                            break;
                    }
                    break;
                case SDL_KEYDOWN:
                    if (event.key.keysym.sym == SDLK_ESCAPE) 
                        quit = true;
                    break;
                case SDL_QUIT:
                    quit = true;
                    break;
                default:
                    break;
            }
        }
        if (visible == true)
        {
            draw_scene();
        }
    }

    engine_sdl_quit();
    engine_sdl_quit(&main_window, &glcontexte);
    return 0;

    (void)N; (void)T;
}
