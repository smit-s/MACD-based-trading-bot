import React, { useState } from "react";
import { CREATE_USER_MUTATION } from "../GraphQL/Mutations";
import { useMutation } from "@apollo/client";

function Form() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [dateOfBirth, setDob] = useState("");
  const [encryptedUserId, setEui] = useState("");
  const [encryptedPassword, setEp] = useState("");
  const [key, setKey] = useState("");
  const [longWindow, setLw] = useState("");
  const [shortWindow, setSw] = useState("");
  const [signal, setSig] = useState("");
  const [seriesLen, setSL] = useState("");
  const [scripCode, setSC] = useState("");
  const [macdLimit, setMacd] = useState("");
  const [scripNum, setSn] = useState("");
  const [tradeQty, setTq] = useState("");
  const [gap, setGap] = useState("");
  const [tickTime, setTt] = useState("");

  const [createUser, { error }] = useMutation(CREATE_USER_MUTATION);

  const addUser = () => {
    createUser({
      variables: {
        email:  email,
        password:  password,
        dateOfBirth:  dateOfBirth,
        encryptedUserId:  encryptedUserId,
        encryptedPassword:  encryptedPassword,
        key:  key,
        shortWindow: shortWindow,
        longWindow: longWindow,
        signal: signal,
        series_len :series_len,
        macdLimit: macdLimit,
        scripCode: scripCode,
        scripNum: scripNum,
        tradeQty: tradeQty,
        gap: gap,
        tickTime: tickTime
      },
    });

    if (error) {
      console.log(error);
    }
  };
  return (
    <div>
      <input
        type="text"
        placeholder="Email"
        onChange={(e) => {
          setEmail(e.target.value);
        }}
      /><br/>
      <input
        type="text"
        placeholder="Password"
        onChange={(e) => {
          setPassword(e.target.value);
        }}
      /><br/>
      <input
        type="text"
        placeholder="DOB"
        onChange={(e) => {
          setDob(e.target.value);
        }}
      /><br/>
      <input
        type="text"
        placeholder="Encrypted User Id"
        onChange={(e) => {
          setEui(e.target.value);
        }}
      /> <br/> <input
          type="text"
          placeholder="Encrypted Password"
          onChange={(e) => {
            setEp(e.target.value);
          }}
        /> <br/> <input
            type="text"
            placeholder="key"
            onChange={(e) => {
              setKey(e.target.value);
            }}
          />  <br/><input
              type="text"
              placeholder="Short window"
              onChange={(e) => {
                setSw(e.target.value);
              }}
            /> <br/> <input
                type="text"
                placeholder="Long Window"
                onChange={(e) => {
                  setLw(e.target.value);
                }}
              /> <br/> <input
                  type="text"
                  placeholder="signal"
                  onChange={(e) => {
                    setSig(e.target.value);
                  }}
                />  <br/><input
                    type="text"
                    placeholder="Series Length"
                    onChange={(e) => {
                      setSL(e.target.value);
                    }}
                  /><br/>  <input
                      type="text"
                      placeholder="macd Limit"
                      onChange={(e) => {
                        setMacd(e.target.value);
                      }}
                    /> <br/> <input
                        type="text"
                        placeholder="scrip code"
                        onChange={(e) => {
                          setSC(e.target.value);
                        }}
                      /> <br/> <input
                          type="text"
                          placeholder="scrip num"
                          onChange={(e) => {
                            setSn(e.target.value);
                          }}
                        /><br/>
                        <input
                            type="text"
                            placeholder="scrip num"
                            onChange={(e) => {
                              setSn(e.target.value);
                            }}
                          /><br/><input
                              type="text"
                              placeholder="scrip num"
                              onChange={(e) => {
                                setSn(e.target.value);
                              }}
                            /><br/><input
                                type="text"
                                placeholder="scrip num"
                                onChange={(e) => {
                                  setSn(e.target.value);
                                }}
                              /><br/>
                              <input
                                  type="text"
                                  placeholder="Trade Quantity"
                                  onChange={(e) => {
                                    setTq(e.target.value);
                                  }}
                                /><br/>
                                <input
                                    type="text"
                                    placeholder="gap"
                                    onChange={(e) => {
                                      setGap(e.target.value);
                                    }}
                                  /><br/>
                                  <input
                                      type="text"
                                      placeholder="tick Time"
                                      onChange={(e) => {
                                        setTt(e.target.value);
                                      }}
                                    /><br/>
      <button onClick={addUser}> Create User</button>
    </div>
  );
}

export default Form;
