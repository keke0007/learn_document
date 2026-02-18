import React, { useState, useEffect, useMemo, useCallback } from 'react';

/**
 * React 组件示例
 * 演示 Hooks、性能优化、事件处理等
 */
function UserList({ users, onUserSelect }) {
  const [filter, setFilter] = useState('');
  const [selectedUserId, setSelectedUserId] = useState(null);
  
  // useMemo：缓存计算结果
  const filteredUsers = useMemo(() => {
    if (!filter) {
      return users;
    }
    return users.filter(user =>
      user.name.toLowerCase().includes(filter.toLowerCase()) ||
      user.email.toLowerCase().includes(filter.toLowerCase())
    );
  }, [users, filter]);
  
  // useCallback：缓存函数
  const handleUserClick = useCallback((userId) => {
    setSelectedUserId(userId);
    if (onUserSelect) {
      onUserSelect(userId);
    }
  }, [onUserSelect]);
  
  // useEffect：副作用处理
  useEffect(() => {
    document.title = `Users: ${filteredUsers.length}`;
    
    return () => {
      document.title = 'React App';
    };
  }, [filteredUsers.length]);
  
  return (
    <div className="user-list">
      <div className="filter">
        <input
          type="text"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          placeholder="搜索用户..."
        />
      </div>
      <ul className="user-items">
        {filteredUsers.map(user => (
          <UserItem
            key={user.id}
            user={user}
            isSelected={selectedUserId === user.id}
            onClick={handleUserClick}
          />
        ))}
      </ul>
      <div className="summary">
        显示 {filteredUsers.length} / {users.length} 个用户
      </div>
    </div>
  );
}

// 使用 React.memo 优化子组件
const UserItem = React.memo(function UserItem({ user, isSelected, onClick }) {
  const handleClick = () => {
    onClick(user.id);
  };
  
  return (
    <li
      className={`user-item ${isSelected ? 'selected' : ''}`}
      onClick={handleClick}
    >
      <div className="avatar">
        <img src={user.avatar} alt={user.name} />
      </div>
      <div className="info">
        <h3>{user.name}</h3>
        <p>{user.email}</p>
        <p>{user.department}</p>
      </div>
    </li>
  );
}, (prevProps, nextProps) => {
  // 自定义比较函数
  return (
    prevProps.user.id === nextProps.user.id &&
    prevProps.isSelected === nextProps.isSelected
  );
});

// 自定义 Hook：useFetch
function useFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    let cancelled = false;
    
    setLoading(true);
    setError(null);
    
    fetch(url)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        if (!cancelled) {
          setData(data);
          setLoading(false);
        }
      })
      .catch(error => {
        if (!cancelled) {
          setError(error);
          setLoading(false);
        }
      });
    
    return () => {
      cancelled = true;
    };
  }, [url]);
  
  return { data, loading, error };
}

// 使用自定义 Hook 的组件
function UserProfile({ userId }) {
  const { data, loading, error } = useFetch(`/api/users/${userId}`);
  
  if (loading) {
    return <div>Loading...</div>;
  }
  
  if (error) {
    return <div>Error: {error.message}</div>;
  }
  
  if (!data) {
    return <div>No data</div>;
  }
  
  return (
    <div className="user-profile">
      <h2>{data.name}</h2>
      <p>{data.email}</p>
      <p>{data.department}</p>
    </div>
  );
}

export default UserList;
