import React from "react";

interface IProps {
  error: Error;
}
export default function FetchError({ error }: IProps) {
  return (
    <div className="flex flex-col gap-5">
      <h1 className="text-xl">There was an error when trying to fetch...</h1>
      <span>{error.message}</span>
    </div>
  );
}
