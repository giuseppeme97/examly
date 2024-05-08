import { Home } from './Home';
import GlobalContext from "./GlobalContext";

function App() {
  // const port = process.env.REACT_APP_PORT;
  // const host = process.env.REACT_APP_HOST;
  const port = "8000";
  const host = "http://localhost";
  const url = `${host}:${port}`;
  const prefix = '/action';

  const appContext = {
    HOST: host,
    DOWNLOAD_TEMPLATE_PATH: url + prefix + '/download-template/',
    LOAD_SOURCE_PATH: url + prefix + '/load-source/',
    GENERATE_EXAMS_PATH: url + prefix + '/generate-exams/',
    TEMPLATE_NAME: 'Template.xlsx',
    BODY_FIELD_FILE: 'file_object',
    ERROR_TEMPLATE: () => alert("Errore nel download del template, riprovare."),
    ERROR_LOAD_SOURCE: () => alert("Errore nel caricamento della sorgente delle domande, riprovare."),
    ERROR_SETTINGS: () => alert("Rivedere i campi inseriti e riprovare."),
    ERROR_GENERATION: () => alert("Errore nella generazione degli esami, riprovare.")
  };

  return (
    <>
      <GlobalContext.Provider value={appContext}>
        <Home />
      </GlobalContext.Provider>
    </>
  )
}

export default App;
