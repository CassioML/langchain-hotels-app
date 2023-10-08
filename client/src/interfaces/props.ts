import { Dispatch, SetStateAction } from "react";

import {NavPage} from "./enums";

export interface LoginProps {
  setUserId: Dispatch<SetStateAction<string|undefined>>;
  setCurrentNavPage: Dispatch<SetStateAction<NavPage>>;
}
