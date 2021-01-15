import React from 'react';
import { BrowserRouter, Route } from 'react-router-dom';
import './App.css';
import SideNav from './Components/SideNav/SideNav';
import PostsPreview from './Pages/PostsPreview/PostsPreview';
import PostsTable from './Pages/PostsTable/PostsTable';

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <SideNav>
          <Route path="/" exact component={PostsPreview} />
          <Route path="/list-table" component={PostsTable} />
        </SideNav>
      </div>
    </BrowserRouter>
  );
}

export default App;
