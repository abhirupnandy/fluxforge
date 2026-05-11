import {
  Component,
  type ErrorInfo,
  type ReactNode,
} from "react";

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
  }

  static getDerivedStateFromError(): State {
    return {
      hasError: true,
    }
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error(error, info)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex h-screen items-center justify-center">
          <div className="rounded-2xl border border-red-900 bg-slate-900 p-8">
            <h1 className="text-3xl font-bold text-red-500">
              Application Error
            </h1>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}