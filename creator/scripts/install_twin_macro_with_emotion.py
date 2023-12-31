from creator.checks import pnpm_is_available, prettier_is_available
from creator.script import Script, TextFile, JsonFileModify

install_twin_macro_with_emotion = Script(
    title="install emotion + twin macro",
    checks=[
        pnpm_is_available,
        prettier_is_available,
    ],
    steps=[
        "(cd ${PROJECT_NAME} && ${PNPM} add @emotion/react @emotion/styled)",
        "(cd ${PROJECT_NAME} && ${PNPM} add --save-dev twin.macro @emotion/babel-plugin-jsx-pragmatic @babel/plugin-transform-react-jsx babel-plugin-macros tailwindcss)",
        TextFile(
            "${PROJECT_NAME}/src/Styles/GlobalStyles.tsx",
            """import { Global } from '@emotion/react'
import tw, { css, theme, GlobalStyles as BaseStyles } from 'twin.macro'
import './main.css'

const customStyles = css({
  body: {
    WebkitTapHighlightColor: theme`colors.purple.500`,
    ...tw`antialiased`,
  },
})

const GlobalStyles = () => (
  <>
    <BaseStyles />
    <Global styles={customStyles} />
  </>
)

export default GlobalStyles""",
            mkdir=True,
        ),
        TextFile(
            "${PROJECT_NAME}/src/main.tsx",
            """import { createRoot } from 'react-dom/client'
import {StrictMode} from 'react'
import GlobalStyles from './Styles/GlobalStyles'
import App from './App'

const container = document.getElementById('root')
const root = createRoot(container!)
root.render(
  <StrictMode>
    <GlobalStyles />
    <App />
  </StrictMode>,
)""",
        ),
        JsonFileModify(
            "${PROJECT_NAME}/package.json",
            lambda data: {**data, "babelMacros": {"twin": {"preset": "emotion"}}},
        ),
        TextFile(
            "${PROJECT_NAME}/vite.config.ts",
            """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  optimizeDeps: {
    esbuildOptions: {
      target: 'es2020',
    },
  },
  esbuild: {
    jsxInject: `import React from 'react'`,
    // https://github.com/vitejs/vite/issues/8644#issuecomment-1159308803
    logOverride: { 'this-is-undefined-in-esm': 'silent' },
  },
  plugins: [
    react({
      babel: {
        plugins: [
          'babel-plugin-macros',
          [
            '@emotion/babel-plugin-jsx-pragmatic',
            {
              export: 'jsx',
              import: '__cssprop',
              module: '@emotion/react',
            },
          ],
          [
            '@babel/plugin-transform-react-jsx',
            { pragma: '__cssprop' },
            'twin.macro',
          ],
        ],
      },
    }),
  ],
})""",
        ),
        "(cd ${PROJECT_NAME} && ${PNPM} add -D @types/react)",
        "(cd ${PROJECT_NAME} && mkdir types)",
        TextFile(
            "${PROJECT_NAME}/types/twin.d.ts",
            """import 'twin.macro'
import { css as cssImport } from '@emotion/react'
import styledImport from '@emotion/styled'
import { CSSInterpolation } from '@emotion/serialize'

declare module 'twin.macro' {
  // The styled and css imports
  const styled: typeof styledImport
  const css: typeof cssImport
}

declare module 'react' {
  // The tw and css prop
  interface DOMAttributes<T> {
    tw?: string
    css?: CSSInterpolation
  }
}""",
        ),
        JsonFileModify(
            "${PROJECT_NAME}/tsconfig.json",
            lambda data: {
                **data,
                "compilerOptions": {
                    **data["compilerOptions"],
                    "skipLibCheck": True,
                    "jsxImportSource": "@emotion/react",
                },
                "include": list(set(data["include"]) | {"types"}),
            },
        ),
        TextFile(
            "${PROJECT_NAME}/src/App.tsx",
            """import tw, { styled } from "twin.macro";

const StyledApp = styled.main(() => [tw`text-3xl font-bold underline`]);

export default function App() {
  return <StyledApp>Hello, world.</StyledApp>;
}
""",
        ),
    ],
)
