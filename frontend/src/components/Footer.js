import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-gradient-to-t from-[#0f0f1e] to-transparent border-t border-purple-500/20 mt-20">
      <div className="container py-10">
        <div className="grid grid-cols-3 gap-8 mb-8">
          <div>
            <h3 className="text-lg font-bold mb-4 gradient-text">KPGM</h3>
            <p className="text-gray-400">Універсальний генератор музики та відео</p>
          </div>
          <div>
            <h4 className="text-sm font-bold mb-4">Посилання</h4>
            <ul className="space-y-2 text-gray-400">
              <li><a href="#" className="hover:text-purple-400">Документація</a></li>
              <li><a href="#" className="hover:text-purple-400">API</a></li>
              <li><a href="#" className="hover:text-purple-400">GitHub</a></li>
            </ul>
          </div>
          <div>
            <h4 className="text-sm font-bold mb-4">Контакти</h4>
            <p className="text-gray-400 text-sm">support@kpgm.io</p>
          </div>
        </div>
        <div className="border-t border-purple-500/20 pt-8 text-center text-gray-400 text-sm">
          <p>&copy; 2026 KPGM KEYPOWERGRAILMYSTERY. Усі права захищені.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
