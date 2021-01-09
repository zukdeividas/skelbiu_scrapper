import React from 'react';
import './App.css';
import SideNav from './Components/SideNav/SideNav';
import PostsPreview from './Pages/PostsPreview/PostsPreview';

function App() {
  return (
    <div className="App">
      <SideNav>
        <PostsPreview></PostsPreview>
      </SideNav>
    </div>
  );
}

export default App;
