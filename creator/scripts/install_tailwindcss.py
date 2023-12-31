from creator.checks import pnpm_is_available, npx_is_available
from creator.script import Script, JavascriptModuleFile, TextFile

install_tailwindcss = Script(
    title="install tailwindcss",
    checks=[
        pnpm_is_available,
        npx_is_available,
    ],
    steps=[
        "(cd ${PROJECT_NAME} && ${PNPM} add -D tailwindcss postcss autoprefixer)",
        "(cd ${PROJECT_NAME} && ${NPX} tailwindcss init -p)",
        JavascriptModuleFile(
            "${PROJECT_NAME}/tailwind.config.js",
            preamble="/** @type {import('tailwindcss').Config} */\n\n",
            json={
                "content": [
                    "./index.html",
                    "./src/**/*.{js,ts,jsx,tsx}",
                ],
                "theme": {
                    "extend": {},
                },
                "plugins": [],
            },
        ),
        TextFile(
            "${PROJECT_NAME}/src/Styles/main.css",
            "@tailwind base;\n@tailwind components;\n@tailwind utilities;\n",
        ),
        TextFile(
            "${PROJECT_NAME}/src/App.tsx",
            (
                "export default function App() {\n"
                "  return (\n"
                '    <h1 className="text-3xl font-bold underline">\n'
                "      Hello, world.\n"
                "    </h1>\n"
                "  )\n"
                "}"
            ),
        ),
    ],
)
