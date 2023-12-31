from creator.checks import pnpm_is_available
from creator.script import Script, TextFile, JsonFileModify

install_ladle = Script(
    title="install ladle",
    checks=[pnpm_is_available],
    steps=[
        "(cd ${PROJECT_NAME} && ${PNPM} add -D typescript@'>= 4.7.x <= 5.2.x' @ladle/react)",
        TextFile(
            "${PROJECT_NAME}/src/App.stories.tsx",
            """import App from './App';
            
export const HelloWorld = () => <App />;""",
        ),
        TextFile(
            "${PROJECT_NAME}/.ladle/components.tsx",
            """import { GlobalProvider } from "@ladle/react";
import GlobalStyles from "../src/Styles/GlobalStyles";

export const Provider: GlobalProvider = ({ children, globalState }) => {
  return (
    <>
      <GlobalStyles />
      {children}
    </>
  );
};
""",
            mkdir=True,
        ),
        TextFile(
            "${PROJECT_NAME}/.ladle/config.mjs",
            """/** @type {import('@ladle/react').UserConfig} */
export default {};""",
        ),
        JsonFileModify(
            "${PROJECT_NAME}/package.json",
            lambda data: {
                **data,
                "scripts": {
                    **data["scripts"],
                    "storybook": "pnpm run storybook:serve",
                    "storybook:serve": "ladle serve",
                    "storybook:build": "ladle build",
                    "storybook:preview": "ladle preview",
                },
            },
        ),
    ],
)
