from creator.checks import pnpm_is_available
from creator.script import Script, TextFile

generate_vite_project = Script(
    title="generate vite project",
    checks=[
        pnpm_is_available,
    ],
    steps=[
        "rm -rf ${PROJECT_NAME}",
        "${PNPM} create vite --template react-ts ${PROJECT_NAME}",
        "(cd ${PROJECT_NAME} && ${PNPM} install)",
        TextFile("${PROJECT_NAME}/src/Styles/main.css", "", mkdir=True),
        TextFile(
            "${PROJECT_NAME}/src/App.tsx",
            (
                "export default function App() {\n"
                "  return <h1>Hello, world</h1>\n"
                "}"
            ),
        ),
        TextFile(
            "${PROJECT_NAME}/src/main.tsx",
            """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './Styles/main.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
""",
        ),
        "rm ${PROJECT_NAME}/src/App.css ${PROJECT_NAME}/src/index.css",
    ],
)
