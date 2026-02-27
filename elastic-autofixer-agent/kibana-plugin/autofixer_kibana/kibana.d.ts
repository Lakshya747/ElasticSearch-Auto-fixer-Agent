declare module 'kibana/server' {
  export interface PluginInitializerContext {
    logger: {
      get: () => Logger;
    };
  }
  export interface CoreSetup {
    http: {
      createRouter: () => IRouter;
    };
  }
  export interface CoreStart {
    http: {
      get: (path: string, options?: any) => Promise<any>;
      post: (path: string, body?: any, options?: any) => Promise<any>;
    };
  }
  export interface Logger {
    info: (msg: string) => void;
    error: (msg: string) => void;
  }
  export interface IRouter {
    get: (options: any, handler: (context: any, request: any, response: any) => Promise<any>) => void;
    post: (options: any, handler: (context: any, request: any, response: any) => Promise<any>) => void;
  }
  export interface Plugin<TSetup, TStart> {
    setup(core: CoreSetup): TSetup;
    start(core: CoreStart): TStart;
    stop?(): void;
  }
}

declare module 'kibana/public' {
  export interface CoreSetup {
    application: {
      register: (options: any) => void;
    };
  }
  export interface CoreStart {
    http: {
      get: (path: string) => Promise<any>;
      post: (path: string, body: any) => Promise<any>;
    };
  }
  export interface AppMountParameters {
    element: HTMLElement;
  }
  // Add Plugin interface here
  export interface Plugin<TSetup, TStart> {
    setup(core: CoreSetup): TSetup;
    start(core: CoreStart): TStart;
    stop?(): void;
  }
}